from ortools.sat.python import cp_model


class BlockOptimizationModel:

    def __init__(self):
        self.model = cp_model.CpModel()
        self.variables = {}

    # ============================================================
    # CREATE DECISION VARIABLES
    # ============================================================

    def create_decision_variables(self, candidates):
        """
        Create one binary decision variable for each
        candidate block.

        1 = candidate selected
        0 = candidate rejected
        """

        for candidate in candidates:

            candidate_id = candidate["candidate_block"]

            self.variables[candidate_id] = (
                self.model.NewBoolVar(
                    f"select_block_{candidate_id}"
                )
            )

        return self.variables

    # ============================================================
    # ADD CANDIDATE CONFLICT CONSTRAINTS
    # ============================================================

    def add_conflict_constraints(self, candidates):
        """
        Prevent selection of two candidate blocks that
        overlap on the same corridor and date.

        If Candidate A and Candidate B overlap:

            xA + xB <= 1

        Therefore OR-Tools can select at most one.
        """

        for i in range(len(candidates)):

            candidate_a = candidates[i]

            for j in range(i + 1, len(candidates)):

                candidate_b = candidates[j]

                # ------------------------------------------------
                # Different corridors cannot conflict
                # ------------------------------------------------

                if (
                    candidate_a["corridor_id"]
                    != candidate_b["corridor_id"]
                ):
                    continue

                # ------------------------------------------------
                # Different dates cannot conflict
                # ------------------------------------------------

                if (
                    candidate_a["block_date"]
                    != candidate_b["block_date"]
                ):
                    continue

                # ------------------------------------------------
                # Check time overlap
                # ------------------------------------------------

                overlap = (
                    candidate_a["start_time"]
                    < candidate_b["end_time"]
                    and
                    candidate_b["start_time"]
                    < candidate_a["end_time"]
                )

                if not overlap:
                    continue

                # ------------------------------------------------
                # Add conflict constraint
                # ------------------------------------------------

                variable_a = self.variables[
                    candidate_a["candidate_block"]
                ]

                variable_b = self.variables[
                    candidate_b["candidate_block"]
                ]

                self.model.Add(
                    variable_a + variable_b <= 1
                )

    # ============================================================
    # ADD OBJECTIVE
    # ============================================================

    def add_objective(self, candidates):
        """
        Maximize the overall quality of selected
        maintenance blocks.

        Higher priority, better coordination and
        time savings increase the score.

        Train conflicts, goods conflicts and long
        blocks reduce the score.
        """

        objective_terms = []

        for candidate in candidates:

            candidate_id = candidate["candidate_block"]

            variable = self.variables[candidate_id]

            # ----------------------------------------------------
            # Maintenance priority
            # ----------------------------------------------------

            priority_score = candidate.get(
                "priority_score",
                0
            )

            # ----------------------------------------------------
            # Department coordination
            # ----------------------------------------------------

            department_count = candidate.get(
                "department_count",
                1
            )

            coordination_bonus = (
                department_count * 20
            )

            # ----------------------------------------------------
            # Time saving
            # ----------------------------------------------------

            time_saving = candidate.get(
                "time_saving",
                0
            )

            time_saving_bonus = (
                time_saving * 10
            )

            # ----------------------------------------------------
            # Train conflict penalty
            # ----------------------------------------------------

            train_conflicts = candidate.get(
                "train_conflict_count",
                0
            )

            train_penalty = (
                train_conflicts * 100
            )

            # ----------------------------------------------------
            # Goods traffic penalty
            # ----------------------------------------------------

            goods_conflicts = candidate.get(
                "goods_conflict_count",
                0
            )

            goods_penalty = (
                goods_conflicts * 20
            )

            # ----------------------------------------------------
            # Duration penalty
            # ----------------------------------------------------

            duration = candidate.get(
                "duration_hours",
                0
            )

            duration_penalty = (
                duration * 5
            )

            # ----------------------------------------------------
            # Final score
            # ----------------------------------------------------

            score = (
                priority_score
                + coordination_bonus
                + time_saving_bonus
                - train_penalty
                - goods_penalty
                - duration_penalty
            )

            # CP-SAT works with integer coefficients
            objective_terms.append(
                int(score) * variable
            )

        self.model.Maximize(
            sum(objective_terms)
        )

    # ============================================================
    # SOLVE MODEL
    # ============================================================

    def solve(self):
        """
        Solve the optimization model.
        """

        solver = cp_model.CpSolver()

        status = solver.Solve(
            self.model
        )

        selected_blocks = []

        if status in (
            cp_model.OPTIMAL,
            cp_model.FEASIBLE
        ):

            for candidate_id, variable in (
                self.variables.items()
            ):

                if solver.Value(variable) == 1:

                    selected_blocks.append(
                        candidate_id
                    )

        return {
            "status": solver.StatusName(status),
            "selected_blocks": selected_blocks,
            "objective_value": solver.ObjectiveValue(),
        }