"""remove block request from optimized block

Revision ID: 9ced5ce52b28
Revises: a27720afd8f1
Create Date: 2026-09-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9ced5ce52b28"
down_revision: Union[str, Sequence[str], None] = "a27720afd8f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove the old single-request relationship."""

    op.drop_constraint(
        "optimized_blocks_block_request_id_fkey",
        "optimized_blocks",
        type_="foreignkey",
    )

    op.drop_column(
        "optimized_blocks",
        "block_request_id",
    )


def downgrade() -> None:
    """Restore the old single-request relationship."""

    op.add_column(
        "optimized_blocks",
        sa.Column(
            "block_request_id",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "optimized_blocks_block_request_id_fkey",
        "optimized_blocks",
        "block_requests",
        ["block_request_id"],
        ["block_request_id"],
    )