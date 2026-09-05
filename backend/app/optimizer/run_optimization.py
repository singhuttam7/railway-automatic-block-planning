from collections import Counter

from app.optimizer.block_optimizer import BlockOptimizer
from app.optimizer.optimization_model import BlockOptimizationModel
from app.services.optimized_block_service import OptimizedBlockService


def main():

    optimizer = BlockOptimizer()
    optimized_block_service = OptimizedBlockService()

    try:

        # ========================================================
        # STEP 1: FETCH BLOCK REQUESTS
        # ========================================================

        requests = optimizer.fetch_block_requests()

        print("\n" + "=" * 80)
        print("PHASE 5.6 — OR-TOOLS BLOCK OPTIMIZATION")
        print("=" * 80)

        print(
            f"\nTotal block requests: "
            f"{len(requests)}"
        )

        # ========================================================
        # STEP 2: GROUP OVERLAPPING REQUESTS
        # ========================================================

        groups = (
            optimizer.group_overlapping_requests(
                requests
            )
        )

        print(
            f"Candidate coordinated blocks: "
            f"{len(groups)}"
        )

        # ========================================================
        # STEP 3: ANALYZE TRAIN & GOODS CONSTRAINTS
        # ========================================================

        constraint_results = (
            optimizer.analyze_block_constraints(
                groups
            )
        )

        # ========================================================
        # STEP 4: PREPARE OPTIMIZATION CANDIDATES
        # ========================================================

        candidates = (
            optimizer.prepare_optimization_candidates(
                groups,
                constraint_results
            )
        )

        print(
            f"Optimization candidates: "
            f"{len(candidates)}"
        )

        # ========================================================
        # STEP 5: REMOVE TRAIN-CONFLICT CANDIDATES
        # ========================================================

        feasible_candidates = [
            candidate
            for candidate in candidates
            if candidate["train_conflict_count"] == 0
        ]

        print(
            f"Candidates without train conflicts: "
            f"{len(feasible_candidates)}"
        )

        # ========================================================
        # STEP 6: CREATE OR-TOOLS MODEL
        # ========================================================

        model = BlockOptimizationModel()

        model.create_decision_variables(
            feasible_candidates
        )

        # Only one alternative candidate can be selected
        # for each original request group.
        model.add_group_constraints(
            feasible_candidates
        )

        # Prevent overlapping blocks on the same
        # corridor and date.
        model.add_conflict_constraints(
            feasible_candidates
        )

        # ========================================================
        # STEP 7: ADD OBJECTIVE
        # ========================================================

        model.add_objective(
            feasible_candidates
        )

        # ========================================================
        # STEP 8: SOLVE
        # ========================================================

        result = model.solve()

        # ========================================================
        # STEP 9: DISPLAY OPTIMIZATION RESULT
        # ========================================================

        print("\n" + "=" * 80)
        print("OPTIMIZATION RESULT")
        print("=" * 80)

        print(
            f"\nSolver Status    : "
            f"{result['status']}"
        )

        print(
            f"Objective Value  : "
            f"{result['objective_value']:.2f}"
        )

        print(
            f"Selected Blocks  : "
            f"{len(result['selected_blocks'])}"
        )

        print("\nSelected Candidate IDs:")

        for candidate_id in result["selected_blocks"]:
            print(
                f"  Candidate Block {candidate_id}"
            )

        # ========================================================
        # STEP 10: GET SELECTED CANDIDATE DETAILS
        # ========================================================

        selected_ids = set(
            result["selected_blocks"]
        )

        selected_candidates = [
            candidate
            for candidate in feasible_candidates
            if candidate["candidate_block"] in selected_ids
        ]

        # ========================================================
        # STEP 10.1: VERIFY GROUP CONSTRAINT
        # ========================================================

        selected_group_ids = [
            candidate.get("group_id")
            for candidate in selected_candidates
            if candidate.get("group_id") is not None
        ]

        group_counts = Counter(selected_group_ids)

        duplicate_groups = {
            group_id: count
            for group_id, count in group_counts.items()
            if count > 1
        }

        print("\n" + "=" * 80)
        print("GROUP CONSTRAINT VERIFICATION")
        print("=" * 80)

        print(
            f"\nSelected candidates : "
            f"{len(selected_candidates)}"
        )

        print(
            f"Unique groups       : "
            f"{len(group_counts)}"
        )

        if duplicate_groups:

            print("\nWARNING: Duplicate groups found!")

            for group_id, count in duplicate_groups.items():

                print(
                    f"  Group {group_id}: "
                    f"{count} candidates"
                )

        else:

            print(
                "\nSUCCESS: No group has more than "
                "one selected candidate."
            )

        # ========================================================
        # STEP 11: SAVE SELECTED BLOCKS TO DATABASE
        # ========================================================

        print("\n" + "=" * 80)
        print("SAVING OPTIMIZED BLOCKS")
        print("=" * 80)

        saved_blocks = (
            optimized_block_service.save_optimized_blocks(
                selected_candidates
            )
        )

        print(
            f"\nSuccessfully saved "
            f"{len(saved_blocks)} optimized blocks."
        )

        # ========================================================
        # STEP 12: DISPLAY SELECTED OPTIMIZED BLOCKS
        # ========================================================

        print("\n" + "=" * 80)
        print("SELECTED OPTIMIZED BLOCKS")
        print("=" * 80)

        for candidate in selected_candidates:

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

        # ========================================================
        # STEP 13: DISPLAY DATABASE IDs
        # ========================================================

        print("\n" + "=" * 80)
        print("DATABASE PERSISTENCE")
        print("=" * 80)

        print("\nSaved Optimized Block IDs:")

        for block in saved_blocks:

            print(
                f"  {block.optimized_block_id}"
            )

        print(
            "\nOptimization and database persistence completed."
        )

    except Exception as error:

        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)

        print(
            f"\nOptimization failed:\n{error}"
        )

        raise

    finally:

        optimizer.close()
        optimized_block_service.close()


if __name__ == "__main__":
    main()