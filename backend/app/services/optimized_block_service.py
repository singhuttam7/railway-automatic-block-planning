from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock
from app.models.optimized_block_request import OptimizedBlockRequest


class OptimizedBlockService:

    def __init__(self):
        self.db = SessionLocal()

    # ============================================================
    # GET NEXT OPTIMIZED BLOCK NUMBER
    # ============================================================

    def get_next_block_number(self):
        """
        Get the next available optimized block number.

        Existing:
            OB-0001
            OB-0002
            ...
            OB-0088

        Next:
            OB-0089
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
        Save selected optimized candidates into:

        1. optimized_blocks
        2. optimized_block_requests

        Each optimized block can contain multiple
        original block requests.
        """

        saved_blocks = []

        try:

            # ----------------------------------------------------
            # Get starting ID only once
            # ----------------------------------------------------

            next_number = self.get_next_block_number()

            # ----------------------------------------------------
            # Save each selected candidate
            # ----------------------------------------------------

            for candidate in selected_candidates:

                # ------------------------------------------------
                # Generate unique optimized block ID
                # ------------------------------------------------

                optimized_block_id = (
                    f"OB-{next_number:04d}"
                )

                next_number += 1

                # ------------------------------------------------
                # Create optimized block
                # ------------------------------------------------

                optimized_block = OptimizedBlock(
                    optimized_block_id=optimized_block_id,
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

                saved_blocks.append(
                    optimized_block
                )

            # ----------------------------------------------------
            # Commit everything
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