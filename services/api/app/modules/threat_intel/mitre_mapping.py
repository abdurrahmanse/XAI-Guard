"""
services/api/app/modules/threat_intel/mitre_mapping.py
======================================================
Maps XAI-Guard attack taxonomy to MITRE ATT&CK techniques.
Grounds the ML classifications in standard cybersecurity frameworks.
"""
from __future__ import annotations

from enum import Enum
from pydantic import BaseModel

from app.core.exceptions import ResourceNotFoundException


class AttackType(str, Enum):
    DDOS = "DDOS"
    PORT_SCAN = "PORT_SCAN"
    BRUTE_FORCE = "BRUTE_FORCE"
    BOTNET = "BOTNET"
    WEB_ATTACK = "WEB_ATTACK"
    INFILTRATION = "INFILTRATION"
    BENIGN = "BENIGN"


class MITREInfo(BaseModel):
    technique_id: str
    technique_name: str
    tactic_id: str
    tactic_name: str
    attack_url: str


MITRE_MAPPING: dict[AttackType, MITREInfo] = {
    AttackType.DDOS: MITREInfo(
        technique_id="T1499.001",
        technique_name="Endpoint DoS: OS Exhaustion Flood",
        tactic_id="TA0040",
        tactic_name="Impact",
        attack_url="https://attack.mitre.org/techniques/T1499/001/"
    ),
    AttackType.PORT_SCAN: MITREInfo(
        technique_id="T1046",
        technique_name="Network Service Discovery",
        tactic_id="TA0007",
        tactic_name="Discovery",
        attack_url="https://attack.mitre.org/techniques/T1046/"
    ),
    AttackType.BRUTE_FORCE: MITREInfo(
        technique_id="T1110",
        technique_name="Brute Force",
        tactic_id="TA0006",
        tactic_name="Credential Access",
        attack_url="https://attack.mitre.org/techniques/T1110/"
    ),
    AttackType.BOTNET: MITREInfo(
        technique_id="T1571",
        technique_name="Non-Standard Port",
        tactic_id="TA0011",
        tactic_name="Command and Control",
        attack_url="https://attack.mitre.org/techniques/T1571/"
    ),
    AttackType.WEB_ATTACK: MITREInfo(
        technique_id="T1190",
        technique_name="Exploit Public-Facing Application",
        tactic_id="TA0001",
        tactic_name="Initial Access",
        attack_url="https://attack.mitre.org/techniques/T1190/"
    ),
    AttackType.INFILTRATION: MITREInfo(
        technique_id="T1078",
        technique_name="Valid Accounts",
        tactic_id="TA0001",
        tactic_name="Initial Access",
        attack_url="https://attack.mitre.org/techniques/T1078/"
    ),
}


def get_mitre_info(attack_type: AttackType | str) -> MITREInfo:
    """
    Retrieve MITRE ATT&CK context for a given attack classification.
    Raises ResourceNotFoundException if the attack type is unknown.
    """
    if isinstance(attack_type, str):
        try:
            attack_type = AttackType(attack_type.upper())
        except ValueError:
            raise ResourceNotFoundException(f"Unknown attack type: {attack_type}")
            
    if attack_type == AttackType.BENIGN:
        raise ResourceNotFoundException("Benign traffic does not map to MITRE ATT&CK.")
        
    info = MITRE_MAPPING.get(attack_type)
    if not info:
        raise ResourceNotFoundException(f"No MITRE mapping found for {attack_type}")
        
    return info
