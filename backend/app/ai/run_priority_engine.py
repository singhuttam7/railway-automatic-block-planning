from datetime import date

from app.database.database import SessionLocal
from app.models.maintenance_task import MaintenanceTask
from app.ai.priority_engine import MaintenancePriorityEngine


def run_priority_engine():
    db = SessionLocal()
    engine = MaintenancePriorityEngine()

    try:
        tasks = db.query(MaintenanceTask).all()

        if not tasks:
            print("No maintenance tasks found.")
            return

        # Start of the planning horizon
        today = date(2026, 9, 5)

        priority_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
        }

        for task in tasks:
            asset = task.asset

            # Get active defects for the asset
            active_defects = [
                defect
                for defect in asset.defects
                if str(defect.status).lower() not in {"resolved", "closed"}
            ]

            # Use the most severe active defect
            if active_defects:
                severity_score = max(
                    defect.severity_score
                    for defect in active_defects
                )

                safety_risk = max(
                    defect.safety_risk
                    for defect in active_defects
                )

                operational_impact = max(
                    defect.operational_impact
                    for defect in active_defects
                )
            else:
                severity_score = 0
                safety_risk = 0
                operational_impact = 0

            # Calculate priority score
            score = engine.calculate_priority(
                criticality=asset.criticality,
                severity_score=severity_score,
                safety_risk=safety_risk,
                operational_impact=operational_impact,
                due_date=task.due_date,
                duration_hours=task.estimated_duration_hours,
                today=today,
            )

            # Determine priority level
            level = engine.get_priority_level(score)

            # Store priority information
            task.priority = round(score)
            task.priority_score = score
            task.priority_level = level

            priority_counts[level] += 1

        db.commit()

        print("\n" + "=" * 50)
        print("MAINTENANCE PRIORITY ENGINE")
        print("=" * 50)

        print(f"Total tasks processed: {len(tasks)}")

        print("\nPriority Distribution:")
        print(f"Critical : {priority_counts['Critical']}")
        print(f"High     : {priority_counts['High']}")
        print(f"Medium   : {priority_counts['Medium']}")
        print(f"Low      : {priority_counts['Low']}")

        print("\nPriority calculation completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error running priority engine: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run_priority_engine()