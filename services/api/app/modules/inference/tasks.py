import logging
import uuid
import time
from app.core.celery_app import celery_app
from app.core.database import get_db

logger = logging.getLogger(__name__)

@celery_app.task(name="app.modules.inference.tasks.run_shadow_inference")
def run_shadow_inference(features_dict: dict, prediction_id: str, champion_attack_type: str, champion_confidence: float):
    """
    Runs the Challenger model(s) in shadow mode silently to compare against the Champion.
    This does NOT block real-time inference latency.
    """
    logger.info(f"Running shadow inference for prediction_id: {prediction_id}")
    try:
        # Mocking Challenger Model Inference
        time.sleep(0.01) # Mock 10ms challenger inference latency
        
        # In reality we would fetch the challenger model from the registry
        challenger_model_version = "lightgbm-v3"
        challenger_attack_type = "DDOS"
        challenger_confidence = champion_confidence * 0.95 # Simulated slight variation
        
        is_discrepancy = champion_attack_type != challenger_attack_type
        
        # Log to MLflow Evaluation or a PostgreSQL Shadow_Mode_Metrics table
        if is_discrepancy:
            logger.warning(f"Shadow Mode Discrepancy! Champion: {champion_attack_type}, Challenger: {challenger_attack_type}")
        else:
            logger.info(f"Shadow Mode Aligned. Challenger Confidence: {challenger_confidence:.2f}")
            
        return {
            "prediction_id": prediction_id,
            "champion_attack_type": champion_attack_type,
            "challenger_attack_type": challenger_attack_type,
            "challenger_confidence": challenger_confidence,
            "discrepancy": is_discrepancy
        }
    except Exception as e:
        logger.error(f"Shadow inference failed: {e}")
        return {"error": str(e)}
