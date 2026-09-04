from datetime import datetime

from app.database.database import SessionLocal
from app.models.block_request import BlockRequest
from app.models.maintenance_task import MaintenanceTask
from app.models.train import Train
from app.models.goods_forecast import GoodsForecast


class BlockOptimizer:

    def __init__(self):
        self.db = SessionLocal()

    # ============================================================
    # 5.2 FETCH BLOCK REQUESTS
    # ============================================================

    def fetch_block_requests(self):
        """
        Fetch block requests along with their
        maintenance task priority information.
        """

        requests = (
            self.db.query(BlockRequest, MaintenanceTask)
            .join(
                MaintenanceTask,
                BlockRequest.task_id == MaintenanceTask.task_id
            )
            .order_by(
                BlockRequest.requested_date,
                BlockRequest.start_time
            )
            .all()
        )

        return requests

    # ============================================================
    # 5.5 FETCH TRAINS
    # ============================================================

    def fetch_trains(self, corridor_id, block_date):
        """
        Fetch trains operating on a specific
        corridor and date.
        """

        trains = (
            self.db.query(Train)
            .filter(
                Train.corridor_id == corridor_id,
                Train.date == block_date
            )
            .order_by(
                Train.start_time
            )
            .all()
        )

        return trains

    # ============================================================
    # 5.5 CHECK BLOCK-TRAIN CONFLICT
    # ============================================================

    def block_conflicts_with_train(
        self,
        block_start,
        block_end,
        train
    ):
        """
        Check whether a candidate block overlaps
        with a scheduled train.
        """

        return (
            block_start < train.end_time
            and train.start_time < block_end
        )

    # ============================================================
    # 5.5 FETCH GOODS FORECASTS
    # ============================================================

    def fetch_goods_forecasts(
        self,
        corridor_id,
        block_date
    ):
        """
        Fetch goods-train forecasts for a specific
        corridor and date.
        """

        forecasts = (
            self.db.query(GoodsForecast)
            .filter(
                GoodsForecast.corridor_id == corridor_id,
                GoodsForecast.date == block_date
            )
            .order_by(
                GoodsForecast.start_time
            )
            .all()
        )

        return forecasts

    # ============================================================
    # 5.5 CHECK BLOCK-GOODS CONFLICT
    # ============================================================

    def block_conflicts_with_goods(
        self,
        block_start,
        block_end,
        forecast
    ):
        """
        Check whether a candidate block overlaps
        with a goods-train forecast window.
        """

        return (
            block_start < forecast.end_time
            and forecast.start_time < block_end
        )

    # ============================================================
    # 5.5 ANALYZE BLOCK CONSTRAINTS
    # ============================================================

    def analyze_block_constraints(self, groups):
        """
        Check candidate blocks against:

        1. Scheduled trains
        2. Goods-train forecasts
        """

        results = []

        for index, group in enumerate(
            groups,
            start=1
        ):

            # ----------------------------------------------------
            # Extract requests
            # ----------------------------------------------------

            requests = [
                item[0]
                for item in group
            ]

            # ----------------------------------------------------
            # Candidate block time
            # ----------------------------------------------------

            start_time = min(
                request.start_time
                for request in requests
            )

            end_time = max(
                request.end_time
                for request in requests
            )

            # ----------------------------------------------------
            # Corridor and date
            # ----------------------------------------------------

            corridor_id = requests[0].corridor_id
            block_date = requests[0].requested_date

            # ----------------------------------------------------
            # Fetch scheduled trains
            # ----------------------------------------------------

            trains = self.fetch_trains(
                corridor_id,
                block_date
            )

            # ----------------------------------------------------
            # Fetch goods-train forecasts
            # ----------------------------------------------------

            goods_forecasts = self.fetch_goods_forecasts(
                corridor_id,
                block_date
            )

            # ----------------------------------------------------
            # Find train conflicts
            # ----------------------------------------------------

            train_conflicts = [
                train
                for train in trains
                if self.block_conflicts_with_train(
                    start_time,
                    end_time,
                    train
                )
            ]

            # ----------------------------------------------------
            # Find goods forecast conflicts
            # ----------------------------------------------------

            goods_conflicts = [
                forecast
                for forecast in goods_forecasts
                if self.block_conflicts_with_goods(
                    start_time,
                    end_time,
                    forecast
                )
            ]

            # ----------------------------------------------------
            # Store analysis result
            # ----------------------------------------------------

            results.append(
                {
                    "candidate_block": index,
                    "corridor_id": corridor_id,
                    "block_date": block_date,
                    "start_time": start_time,
                    "end_time": end_time,
                    "train_conflicts": train_conflicts,
                    "goods_conflicts": goods_conflicts,
                    "train_conflict_count": len(
                        train_conflicts
                    ),
                    "goods_conflict_count": len(
                        goods_conflicts
                    ),
                }
            )

        return results

    # ============================================================
    # 5.6 PREPARE OPTIMIZATION CANDIDATES
    # ============================================================

    def prepare_optimization_candidates(
        self,
        groups,
        constraint_results
    ):
        """
        Convert candidate block groups and their constraint
        analysis into a format suitable for OR-Tools.
        """

        candidates = []

        for index, group in enumerate(
            groups,
            start=1
        ):

            requests = [
                item[0]
                for item in group
            ]

            tasks = [
                item[1]
                for item in group
            ]

            # ----------------------------------------------------
            # Candidate time window
            # ----------------------------------------------------

            start_time = min(
                request.start_time
                for request in requests
            )

            end_time = max(
                request.end_time
                for request in requests
            )

            # ----------------------------------------------------
            # Duration
            # ----------------------------------------------------

            start_datetime = datetime.combine(
                requests[0].requested_date,
                start_time
            )

            end_datetime = datetime.combine(
                requests[0].requested_date,
                end_time
            )

            duration_hours = (
                end_datetime - start_datetime
            ).total_seconds() / 3600

            # ----------------------------------------------------
            # Total requested duration
            # ----------------------------------------------------

            total_requested_duration = sum(
                request.duration_hours
                for request in requests
            )

            # ----------------------------------------------------
            # Time saving
            # ----------------------------------------------------

            time_saving = (
                total_requested_duration
                - duration_hours
            )

            # ----------------------------------------------------
            # Department count
            # ----------------------------------------------------

            departments = {
                task.asset.department_id
                for task in tasks
            }

            department_count = len(
                departments
            )

            # ----------------------------------------------------
            # Priority
            # ----------------------------------------------------

            priority_score = max(
                (
                    task.priority_score
                    if task.priority_score is not None
                    else 0
                )
                for task in tasks
            )

            # ----------------------------------------------------
            # Constraint information
            # ----------------------------------------------------

            constraint = constraint_results[index - 1]

            train_conflict_count = (
                constraint["train_conflict_count"]
            )

            goods_conflict_count = (
                constraint["goods_conflict_count"]
            )

            # ----------------------------------------------------
            # Candidate block
            # ----------------------------------------------------

            candidate = {
                "candidate_block": index,
                "corridor_id": requests[0].corridor_id,
                "block_date": requests[0].requested_date,
                "start_time": start_time,
                "end_time": end_time,
                "duration_hours": duration_hours,
                "time_saving": time_saving,
                "department_count": department_count,
                "priority_score": priority_score,
                "train_conflict_count": train_conflict_count,
                "goods_conflict_count": goods_conflict_count,

                # Original block requests included in
                # this coordinated candidate block.
                "block_request_ids": [
                    request.block_request_id
                    for request in requests
                ],
            }

            candidates.append(
                candidate
            )

        return candidates

    # ============================================================
    # 5.5 DISPLAY CONSTRAINT ANALYSIS
    # ============================================================

    def display_constraint_analysis(self, results):
        """
        Display train and goods-train conflicts
        for candidate blocks.
        """

        print("\n" + "=" * 80)
        print("TRAIN & GOODS-TRAIN CONSTRAINT ANALYSIS")
        print("=" * 80)

        for result in results:

            print(
                f"\nCandidate Block "
                f"{result['candidate_block']}"
            )

            print("-" * 80)

            print(
                f"Corridor        : "
                f"{result['corridor_id']}"
            )

            print(
                f"Date            : "
                f"{result['block_date']}"
            )

            print(
                f"Time            : "
                f"{result['start_time']} - "
                f"{result['end_time']}"
            )

            print(
                f"Train Conflicts : "
                f"{result['train_conflict_count']}"
            )

            print(
                f"Goods Conflicts : "
                f"{result['goods_conflict_count']}"
            )

            # ----------------------------------------------------
            # Determine block status
            # ----------------------------------------------------

            if result["train_conflict_count"] > 0:

                print(
                    "Status          : "
                    "TRAIN CONFLICT ❌"
                )

            elif result["goods_conflict_count"] > 0:

                print(
                    "Status          : "
                    "GOODS TRAFFIC RISK ⚠️"
                )

            else:

                print(
                    "Status          : "
                    "FEASIBLE ✓"
                )

    # ============================================================
    # 5.3 CHECK REQUEST OVERLAP
    # ============================================================

    def requests_overlap(
        self,
        request_a,
        request_b
    ):
        """
        Check whether two block requests overlap.

        Two requests overlap only when:

        1. They are on the same corridor
        2. They are on the same date
        3. Their time intervals overlap
        """

        # Different corridor
        if (
            request_a.corridor_id
            != request_b.corridor_id
        ):
            return False

        # Different date
        if (
            request_a.requested_date
            != request_b.requested_date
        ):
            return False

        # Check time overlap
        return (
            request_a.start_time
            < request_b.end_time
            and
            request_b.start_time
            < request_a.end_time
        )

    # ============================================================
    # 5.4 GROUP OVERLAPPING REQUESTS
    # ============================================================

    def group_overlapping_requests(
        self,
        requests
    ):
        """
        Group block requests that overlap on the same
        corridor and date.

        Each group represents a candidate coordinated block.

        Example:

        ENG : 10:00 - 12:00
        SNT : 10:30 - 11:30
        TRD : 11:00 - 13:00

        Candidate Block:

        10:00 - 13:00
        """

        groups = []

        # Keep track of requests already assigned
        visited = set()

        for i, (
            request_a,
            task_a
        ) in enumerate(requests):

            # Skip already processed request
            if (
                request_a.block_request_id
                in visited
            ):
                continue

            # Start a new group
            group = [
                (
                    request_a,
                    task_a
                )
            ]

            visited.add(
                request_a.block_request_id
            )

            # Continue searching for overlapping requests
            changed = True

            while changed:

                changed = False

                for j, (
                    request_b,
                    task_b
                ) in enumerate(requests):

                    # Already included
                    if (
                        request_b.block_request_id
                        in visited
                    ):
                        continue

                    # Compare request B with
                    # requests already in group
                    for (
                        existing_request,
                        existing_task
                    ) in group:

                        if self.requests_overlap(
                            existing_request,
                            request_b
                        ):

                            group.append(
                                (
                                    request_b,
                                    task_b
                                )
                            )

                            visited.add(
                                request_b.block_request_id
                            )

                            changed = True

                            break

            # Add completed group
            groups.append(group)

        return groups

    # ============================================================
    # DISPLAY CANDIDATE BLOCKS
    # ============================================================

    def display_candidate_blocks(self, candidates):
        print("\n" + "=" * 80)
        print("CANDIDATE BLOCKS")
        print("=" * 80)

        for candidate in candidates:

            print(
                f"\nCandidate Block "
                f"{candidate['candidate_block']}"
            )

            print("-" * 80)

            print(
                f"Corridor          : "
                f"{candidate['corridor_id']}"
            )

            print(
                f"Date              : "
                f"{candidate['block_date']}"
            )

            print(
                f"Time              : "
                f"{candidate['start_time']} - "
                f"{candidate['end_time']}"
            )

            print(
                f"Duration          : "
                f"{candidate['duration_hours']:.2f} hours"
            )

            print(
                f"Priority Score    : "
                f"{candidate['priority_score']:.2f}"
            )

            print(
                f"Departments       : "
                f"{candidate['department_count']}"
            )

            print(
                f"Time Saving       : "
                f"{candidate['time_saving']:.2f} hours"
            )

            print(
                f"Train Conflicts   : "
                f"{candidate['train_conflict_count']}"
            )

            print(
                f"Goods Conflicts   : "
                f"{candidate['goods_conflict_count']}"
            )

            # ----------------------------------------------------
            # Original block requests
            # ----------------------------------------------------

            block_request_ids = candidate.get(
                "block_request_ids",
                []
            )

            if block_request_ids:

                print(
                    f"Block Requests    : "
                    f"{', '.join(block_request_ids)}"
                )

            else:

                print(
                    "Block Requests    : None"
                )

    # ============================================================
    # COORDINATION TEST
    # ============================================================

    def test_coordination_scenario(self):
        """
        Test the known C001 multi-department
        coordination scenario.
        """

        requests = self.fetch_block_requests()

        c001_requests = [
            (
                block_request,
                task
            )
            for block_request, task in requests
            if (
                block_request.corridor_id == "C001"
                and str(
                    block_request.requested_date
                ) == "2026-09-05"
                and block_request.block_request_id
                in {
                    "BR-0001",
                    "BR-0002",
                    "BR-0003"
                }
            )
        ]

        print("\n" + "=" * 80)
        print("COORDINATION TEST — C001")
        print("=" * 80)

        if not c001_requests:

            print(
                "No coordination scenario "
                "requests found."
            )

            return

        for i in range(
            len(c001_requests)
        ):

            request_a, task_a = (
                c001_requests[i]
            )

            for j in range(
                i + 1,
                len(c001_requests)
            ):

                request_b, task_b = (
                    c001_requests[j]
                )

                overlap = (
                    self.requests_overlap(
                        request_a,
                        request_b
                    )
                )

                print(
                    f"{request_a.block_request_id} "
                    f"({task_a.task_id}) <-> "
                    f"{request_b.block_request_id} "
                    f"({task_b.task_id})"
                )

                print(
                    f"Overlap: {overlap}\n"
                )

    # ============================================================
    # DISPLAY ALL BLOCK REQUESTS
    # ============================================================

    def display_requests(self):
        """
        Display all block requests and their
        maintenance priority.
        """

        requests = self.fetch_block_requests()

        print("\n" + "=" * 80)
        print("BLOCK REQUESTS FOR OPTIMIZATION")
        print("=" * 80)

        print(
            f"Total block requests: "
            f"{len(requests)}\n"
        )

        for block_request, task in requests:

            priority_score = (
                task.priority_score
                if task.priority_score is not None
                else 0
            )

            priority_level = (
                task.priority_level
                if task.priority_level is not None
                else "Not Calculated"
            )

            print(
                f"{block_request.block_request_id} | "
                f"{task.task_id} | "
                f"Corridor: "
                f"{block_request.corridor_id} | "
                f"Date: "
                f"{block_request.requested_date} | "
                f"{block_request.start_time} - "
                f"{block_request.end_time} | "
                f"Priority: "
                f"{priority_score:.2f} | "
                f"{priority_level}"
            )

    # ============================================================
    # CLOSE DATABASE
    # ============================================================

    def close(self):
        """
        Close database connection.
        """

        self.db.close()


# =================================================================
# MAIN
# =================================================================

if __name__ == "__main__":

    optimizer = BlockOptimizer()

    try:

        # ---------------------------------------------------------
        # Step 1: Fetch block requests
        # ---------------------------------------------------------

        requests = (
            optimizer.fetch_block_requests()
        )

        # ---------------------------------------------------------
        # Step 2: Display all requests
        # ---------------------------------------------------------

        optimizer.display_requests()

        # ---------------------------------------------------------
        # Step 3: Test C001 coordination scenario
        # ---------------------------------------------------------

        optimizer.test_coordination_scenario()

        # ---------------------------------------------------------
        # Step 4: Group overlapping requests
        # ---------------------------------------------------------

        groups = (
            optimizer.group_overlapping_requests(
                requests
            )
        )

        # ---------------------------------------------------------
        # Display number of groups
        # ---------------------------------------------------------

        print(
            "\nNUMBER OF GROUPS:",
            len(groups)
        )

        for i, group in enumerate(
            groups,
            start=1
        ):

            print(
                f"Group {i}: "
                f"{len(group)} requests"
            )

        # ---------------------------------------------------------
        # Step 5: Analyze constraints
        # ---------------------------------------------------------

        constraint_results = (
            optimizer.analyze_block_constraints(
                groups
            )
        )

        # ---------------------------------------------------------
        # Step 6: Prepare optimization candidates
        # ---------------------------------------------------------

        candidates = (
            optimizer.prepare_optimization_candidates(
                groups,
                constraint_results
            )
        )

        # ---------------------------------------------------------
        # Step 7: Display candidate blocks
        # ---------------------------------------------------------

        optimizer.display_candidate_blocks(
            candidates
        )

        # ---------------------------------------------------------
        # Step 8: Display constraint analysis
        # ---------------------------------------------------------

        optimizer.display_constraint_analysis(
            constraint_results
        )

    finally:

        optimizer.close()