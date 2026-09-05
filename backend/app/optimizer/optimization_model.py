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
    # ADD GROUP MUTUAL-EXCLUSION CONSTRAINTS
    # ============================================================

    def add_group_constraints(self, candidates):
        """
        Ensure that at most ONE candidate is selected
        from each original request/group.

        This is important when alternative time slots are
        generated for the same maintenance request.

        Example:

            Group 5
              Candidate 101 -> 10:00-12:00
              Candidate 102 -> 13:00-15:00
              Candidate 103 -> 16:00-18:00

        OR-Tools can select:

            101 OR 102 OR 103

        but never two or more of them.
        """

        groups = {}

        for candidate in candidates:

            group_id = candidate.get("group_id")

            # Candidates without a group_id are treated
            # as independent candidates.
            if group_id is None:
                continue

            groups.setdefault(group_id, []).append(
                candidate["candidate_block"]
            )

        for group_id, candidate_ids in groups.items():

            variables = [
                self.variables[candidate_id]
                for candidate_id in candidate_ids
            ]

            self.model.Add(
                sum(variables) <= 1
            )

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
    # ADD TRAIN CONFLICT CONSTRAINTS
    # ============================================================

    def add_train_conflict_constraints(self, candidates):
        """
        Train conflicts are treated as HARD constraints.

        A candidate block having one or more train conflicts
        cannot be selected.

        train_conflict_count > 0
            -> candidate rejected

        train_conflict_count == 0
            -> candidate remains feasible
        """

        for candidate in candidates:

            train_conflicts = candidate.get(
                "train_conflict_count",
                0
            )

            if train_conflicts > 0:

                candidate_id = candidate["candidate_block"]

                variable = self.variables[candidate_id]

                self.model.Add(
                    variable == 0
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

        Goods conflicts and long blocks reduce the score.

        Train conflicts are handled as HARD constraints
        and therefore are not selected.
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
            # Train conflicts
            # ----------------------------------------------------

            # Train conflicts are already prohibited by
            # add_train_conflict_constraints().
            #
            # Keep this penalty as an additional safeguard.

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
            # Time deviation penalty
            # ----------------------------------------------------

            time_deviation = candidate.get("time_deviation_hours",0)

            time_deviation_penalty = (time_deviation * 10)

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
                - time_deviation_penalty
            )

            # CP-SAT requires integer coefficients.
            #
            # Multiplying by 100 preserves more precision than
            # directly converting the score to int.

            score_scaled = int(round(score * 100))

            objective_terms.append(
                score_scaled * variable
            )

        # --------------------------------------------------------
        # Maximize objective
        # --------------------------------------------------------

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