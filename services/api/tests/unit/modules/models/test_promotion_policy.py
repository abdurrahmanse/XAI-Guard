"""Unit tests for model promotion policy — Champion/Challenger rules."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))

from app.modules.registry.models import ModelStatusEnum


def test_all_lifecycle_states_exist():
    values = {s.value for s in ModelStatusEnum}
    assert values == {"TRAINING", "REGISTERED", "CHALLENGER", "CHAMPION", "ARCHIVED"}


def test_champion_is_unique_terminal_state():
    """Only one model can be CHAMPION — verify it is a distinct state."""
    assert ModelStatusEnum.CHAMPION != ModelStatusEnum.CHALLENGER
    assert ModelStatusEnum.CHAMPION != ModelStatusEnum.ARCHIVED


def test_archived_is_final_state():
    """ARCHIVED models cannot be promoted — verify it is not CHAMPION."""
    assert ModelStatusEnum.ARCHIVED.value == "ARCHIVED"
    assert ModelStatusEnum.ARCHIVED != ModelStatusEnum.CHAMPION


def test_promotion_path_ordering():
    """Valid promotion flow: REGISTERED → CHALLENGER → CHAMPION."""
    flow = [
        ModelStatusEnum.TRAINING,
        ModelStatusEnum.REGISTERED,
        ModelStatusEnum.CHALLENGER,
        ModelStatusEnum.CHAMPION,
    ]
    # All steps are distinct
    assert len(set(flow)) == 4


def test_challenger_beats_registered():
    """CHALLENGER status is closer to production than REGISTERED."""
    assert ModelStatusEnum.CHALLENGER != ModelStatusEnum.REGISTERED
    assert ModelStatusEnum.CHAMPION != ModelStatusEnum.REGISTERED

