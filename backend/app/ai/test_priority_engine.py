from datetime import date, timedelta

from app.ai.priority_engine import (
    MaintenancePriorityEngine,
)


engine = MaintenancePriorityEngine()


today = date(2026, 9, 3)

score = engine.calculate_priority(
    criticality=10,
    severity_score=8,
    safety_risk=9,
    operational_impact=8,
    due_date=today + timedelta(days=2),
    duration_hours=4,
    today=today,
)

level = engine.get_priority_level(score)


print("Priority Score:", score)
print("Priority Level:", level)