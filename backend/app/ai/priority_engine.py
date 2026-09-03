from datetime import date


class MaintenancePriorityEngine:
    """
    AI-based maintenance priority scoring engine.

    Calculates a priority score (0-100) using:
    - Asset criticality
    - Defect severity
    - Safety risk
    - Operational impact
    - Due-date urgency
    - Maintenance duration
    """

    # Feature weights
    CRITICALITY_WEIGHT = 0.25
    SEVERITY_WEIGHT = 0.20
    SAFETY_WEIGHT = 0.20
    OPERATIONAL_WEIGHT = 0.15
    URGENCY_WEIGHT = 0.15
    DURATION_WEIGHT = 0.05

    @staticmethod
    def normalize(value, minimum, maximum):
        """
        Convert a value into a 0-100 scale.
        """

        if maximum == minimum:
            return 0.0

        score = (
            (value - minimum)
            / (maximum - minimum)
        ) * 100

        return max(0.0, min(100.0, score))

    @staticmethod
    def calculate_urgency(due_date: date, today: date):
        """
        Calculate urgency based on days remaining until
        the maintenance task is due.

        Overdue tasks receive maximum urgency.
        """

        days_remaining = (
            due_date - today
        ).days

        if days_remaining <= 0:
            return 100.0

        if days_remaining <= 3:
            return 90.0

        if days_remaining <= 7:
            return 75.0

        if days_remaining <= 14:
            return 60.0

        if days_remaining <= 30:
            return 40.0

        if days_remaining <= 60:
            return 20.0

        return 10.0

    @staticmethod
    def calculate_duration_score(duration_hours):
        """
        Convert maintenance duration into a 0-100 score.

        Longer tasks receive a higher score because they
        require more careful block planning.
        """

        return MaintenancePriorityEngine.normalize(
            duration_hours,
            minimum=1,
            maximum=8,
        )

    @classmethod
    def calculate_priority(
        cls,
        criticality,
        severity_score,
        safety_risk,
        operational_impact,
        due_date,
        duration_hours,
        today=None,
    ):
        """
        Calculate final maintenance priority score.
        """

        if today is None:
            today = date.today()

        # ---------------------------------------------
        # Normalize individual features
        # ---------------------------------------------

        criticality_score = cls.normalize(
            criticality,
            minimum=4,
            maximum=10,
        )

        severity_score_normalized = cls.normalize(
            severity_score,
            minimum=3,
            maximum=10,
        )

        safety_score = cls.normalize(
            safety_risk,
            minimum=1,
            maximum=10,
        )

        operational_score = cls.normalize(
            operational_impact,
            minimum=1,
            maximum=10,
        )

        urgency_score = cls.calculate_urgency(
            due_date,
            today,
        )

        duration_score = cls.calculate_duration_score(
            duration_hours
        )

        # ---------------------------------------------
        # Weighted final score
        # ---------------------------------------------

        priority_score = (
            criticality_score
            * cls.CRITICALITY_WEIGHT

            + severity_score_normalized
            * cls.SEVERITY_WEIGHT

            + safety_score
            * cls.SAFETY_WEIGHT

            + operational_score
            * cls.OPERATIONAL_WEIGHT

            + urgency_score
            * cls.URGENCY_WEIGHT

            + duration_score
            * cls.DURATION_WEIGHT
        )

        return round(
            priority_score,
            2
        )

    @staticmethod
    def get_priority_level(score):
        if score >= 85:
            return "Critical"
        if score >= 70:
            return "High"
        if score >= 50:
            return "Medium"
        return "Low"