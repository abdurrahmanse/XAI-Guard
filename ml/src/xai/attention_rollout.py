"""
ml/src/xai/attention_rollout.py
================================
Attention Rollout explainer for Transformer and LSTM models.

WHY NOT RAW ATTENTION WEIGHTS?
Jain & Wallace (2019) showed that raw attention weights do NOT reliably
indicate which inputs caused a decision — you can permute attention weights
and still get the same model output in some cases.

WHAT IS ATTENTION ROLLOUT?
Abnar & Zuidema (2020) fix this by recursively multiplying attention matrices
across all Transformer layers, accounting for residual connections:

    Rollout(L) = A(1) × A(2) × ... × A(L)

where each A(l) = 0.5 * attention_weight(l) + 0.5 * Identity
(the 0.5 factor accounts for the residual connection that bypasses attention).

The result is a single importance score per input token/timestep that
properly accounts for how information flows across all layers.

In your paper (§4.4):
"We use Attention Rollout (Abnar & Zuidema, 2020) rather than raw attention
weights, following the finding by Jain & Wallace (2019) that raw attention
does not reliably indicate explanation faithfulness."

Usage:
    from xai.attention_rollout import AttentionRolloutExtractor
    extractor = AttentionRolloutExtractor(transformer_model)
    rollout = extractor.extract(x_sample)   # shape: (seq_len,)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class AttentionRolloutResult:
    """
    Attention Rollout result for a single input sequence.

    Attributes
    ----------
    rollout_scores : np.ndarray
        Shape (seq_len,). Importance score per timestep — higher = more important.
        Normalised so that sum = 1.0.
    predicted_class : int
    predicted_proba : float
    n_layers : int
        Number of Transformer layers used in rollout computation.
    most_attended_timestep : int
        Index of the timestep with the highest rollout score.
    """

    rollout_scores: np.ndarray
    predicted_class: int
    predicted_proba: float
    n_layers: int
    most_attended_timestep: int

    def summary(self) -> str:
        top_3 = np.argsort(self.rollout_scores)[::-1][:3]
        return (
            f"Predicted: class {self.predicted_class} ({self.predicted_proba:.3f})\n"
            f"Most attended timestep: t={self.most_attended_timestep} "
            f"(score={self.rollout_scores[self.most_attended_timestep]:.4f})\n"
            f"Top 3 timesteps: {list(top_3)} with scores {[f'{self.rollout_scores[i]:.4f}' for i in top_3]}"
        )


class AttentionRolloutExtractor:
    """
    Extracts Attention Rollout importance scores from a PyTorch Transformer.

    The model must expose attention weights during forward passes.
    This is done by calling the model's encoder layers with
    `need_weights=True` in the MultiheadAttention call.

    Parameters
    ----------
    model : torch.nn.Module
        A trained Transformer model that exposes attention weights.
        The model should have a `get_attention_weights(x)` method that returns
        a list of attention weight tensors, one per layer.
    device : str
        "cpu" or "cuda" — where to run inference.
    """

    def __init__(self, model: object, device: str = "cpu") -> None:
        try:
            import torch

            self.torch = torch
        except ImportError as exc:
            raise ImportError("torch is required: pip install torch") from exc

        self.model = model
        self.device = device
        model.eval()

    def _compute_rollout(
        self, attention_weights_per_layer: list[np.ndarray]
    ) -> np.ndarray:
        """
        Compute Attention Rollout across all layers.

        Parameters
        ----------
        attention_weights_per_layer : list of (seq_len, seq_len) arrays
            One attention matrix per layer (averaged across heads).

        Returns
        -------
        np.ndarray of shape (seq_len,)
            Normalised rollout scores — the CLS token's attention to each input.
        """
        n_layers = len(attention_weights_per_layer)
        seq_len = attention_weights_per_layer[0].shape[-1]

        # Start with identity matrix
        rollout = np.eye(seq_len)

        for attn in attention_weights_per_layer:
            # attn shape: (seq_len, seq_len) — averaged across heads
            # Add residual connection (Abnar & Zuidema 2020, Eq. 1)
            attn_with_residual = 0.5 * attn + 0.5 * np.eye(seq_len)
            # Normalise rows to sum to 1
            row_sums = attn_with_residual.sum(axis=-1, keepdims=True)
            attn_with_residual = attn_with_residual / (row_sums + 1e-9)
            # Multiply (matrix multiplication, not element-wise)
            rollout = attn_with_residual @ rollout

        # Return the first row (CLS token → all positions)
        scores = rollout[0]
        scores = scores / (scores.sum() + 1e-9)  # normalise to sum = 1
        return scores

    def extract(self, x_sample: np.ndarray) -> AttentionRolloutResult:
        """
        Extract Attention Rollout for a single input sample.

        Parameters
        ----------
        x_sample : np.ndarray
            Shape (seq_len, n_features) for a sequence model,
            or (n_features,) for tabular input (will be expanded).

        Returns
        -------
        AttentionRolloutResult
        """
        torch = self.torch
        model = self.model

        if x_sample.ndim == 1:
            # Tabular input — treat as single-timestep sequence
            x_sample = x_sample.reshape(1, -1)

        x_tensor = torch.FloatTensor(x_sample).unsqueeze(0).to(self.device)

        with torch.no_grad():
            # Attempt to collect attention weights via hook
            attn_weights_list: list[np.ndarray] = []

            def _hook(module, input, output):
                # output[1] is the attention weight tensor for nn.MultiheadAttention
                if (
                    isinstance(output, tuple)
                    and len(output) > 1
                    and output[1] is not None
                ):
                    w = output[1].detach().cpu().numpy()
                    # w shape: (batch, n_heads, seq_len, seq_len) OR (batch, seq_len, seq_len)
                    if w.ndim == 4:
                        w = w[0].mean(axis=0)  # average across heads
                    elif w.ndim == 3:
                        w = w[0]
                    attn_weights_list.append(w)

            hooks = []
            for module in model.modules():
                if module.__class__.__name__ == "MultiheadAttention":
                    hooks.append(module.register_forward_hook(_hook))

            logits = model(x_tensor)
            for h in hooks:
                h.remove()

        # Get prediction
        proba = torch.softmax(logits, dim=-1).cpu().numpy()[0]
        predicted_class = int(np.argmax(proba))
        predicted_proba = float(proba[predicted_class])

        if not attn_weights_list:
            # Model doesn't expose attention weights — return uniform rollout
            seq_len = x_sample.shape[0]
            rollout_scores = np.ones(seq_len) / seq_len
            n_layers = 0
        else:
            rollout_scores = self._compute_rollout(attn_weights_list)
            n_layers = len(attn_weights_list)

        most_attended = int(np.argmax(rollout_scores))

        return AttentionRolloutResult(
            rollout_scores=rollout_scores,
            predicted_class=predicted_class,
            predicted_proba=predicted_proba,
            n_layers=n_layers,
            most_attended_timestep=most_attended,
        )
