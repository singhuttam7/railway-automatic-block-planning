from datetime import datetime

from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock
from app.models.optimized_block_request import OptimizedBlockRequest
from app.models.optimization_run import OptimizationRun


class OptimizedBlockService:

    def __init__(self):
        self.db = SessionLocal()

    # ============================================================
    # GET NEXT OPTIMIZED BLOCK NUMBER
    # ============================================================

    def get_next_block_number(self):
        """
        Get the next available optimized block number.
        """

        blocks = (
            self.db.query(OptimizedBlock.optimized_block_id)
            .all()
        )

        max_number = 0

        for (block_id,) in blocks:
            try:
                number = int(block_id.split("-")[1])

                if number > max_number:
                    max_number = number

            except (IndexError, ValueError):
                continue

        return max_number + 1

    # ============================================================
    # SAVE OPTIMIZED BLOCKS
    # ============================================================

    def save_optimized_blocks(self, selected_candidates):
        """
        Create one optimization run and save all selected
        optimized blocks under that run.

        Also saves relationships between optimized blocks
        and their original block requests.
        """

        saved_blocks = []

        try:
            # ----------------------------------------------------
            # Create a new optimization run
            # ----------------------------------------------------

            optimization_run = OptimizationRun(
                run_date=datetime.now(),
                status="Completed",
            )

            self.db.add(optimization_run)

            # Flush so PostgreSQL generates the run ID
            self.db.flush()

            # ----------------------------------------------------
            # Get starting optimized block ID
            # ----------------------------------------------------

            next_number = self.get_next_block_number()

            # ----------------------------------------------------
            # Save each selected candidate
            # ----------------------------------------------------

            for candidate in selected_candidates:

                # Generate unique optimized block ID
                optimized_block_id = (
                    f"OB-{next_number:04d}"
                )

                next_number += 1

                # ------------------------------------------------
                # Create optimized block
                # ------------------------------------------------

                optimized_block = OptimizedBlock(
                    optimized_block_id=optimized_block_id,
                    optimization_run_id=(
                        optimization_run.optimization_run_id
                    ),
                    corridor_id=candidate["corridor_id"],
                    block_date=candidate["block_date"],
                    start_time=candidate["start_time"],
                    end_time=candidate["end_time"],
                    duration_hours=candidate["duration_hours"],
                    department_count=candidate["department_count"],
                    optimization_score=candidate["priority_score"],
                    status="Planned",
                )

                self.db.add(optimized_block)

                # ------------------------------------------------
                # Save block-request relationships
                # ------------------------------------------------

                block_request_ids = candidate.get(
                    "block_request_ids",
                    []
                )

                for block_request_id in block_request_ids:

                    association = OptimizedBlockRequest(
                        optimized_block_id=optimized_block_id,
                        block_request_id=block_request_id,
                    )

                    self.db.add(association)

                saved_blocks.append(optimized_block)

            # ----------------------------------------------------
            # Commit optimization run + blocks + relationships
            # ----------------------------------------------------

            self.db.commit()

            return saved_blocks

        except Exception:
            self.db.rollback()
            raise

    # ============================================================
    # CLOSE DATABASE
    # ============================================================

    def close(self):
        """
        Close database session.
        """

        self.db.close()