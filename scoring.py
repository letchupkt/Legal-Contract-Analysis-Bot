
from typing import List, Dict

RISK_MAP = {"Low": 1, "Medium": 2, "High": 3}

def clause_risk_score(risk_label: str) -> int:
    return RISK_MAP.get(risk_label, 2)

def overall_risk_score(clauses: List[Dict]) -> float:

    if not clauses:
        return 0.0
    total = sum(clause_risk_score(c.get('risk','Medium')) for c in clauses)
    max_total = len(clauses) * 3
    score = (total / max_total) * 100
    return round(score,1)
