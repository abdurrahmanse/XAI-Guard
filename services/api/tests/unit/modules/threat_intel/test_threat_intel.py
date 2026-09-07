"""Phase 53.3 - Threat Intel Tests"""
import pytest
from app.modules.threat_intel.mitre_mapping import get_mitre_info, AttackType

def test_mitre_mapping():
    info = get_mitre_info(AttackType.DDOS)
    assert info.technique_id == "T1499.001"
    
    info = get_mitre_info("BRUTE_FORCE")
    assert info.technique_id == "T1110"
