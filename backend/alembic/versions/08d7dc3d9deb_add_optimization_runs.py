"""add optimization runs

Revision ID: 08d7dc3d9deb
Revises: 9ced5ce52b28
Create Date: 2026-09-04 15:14:46.508031
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "08d7dc3d9deb"
down_revision: Union[str, Sequence[str], None] = "9ced5ce52b28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create optimization_runs table
    op.create_table(
        "optimization_runs",
        sa.Column(
            "optimization_run_id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "run_date",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("optimization_run_id"),
    )

    # 2. Add the new column temporarily as nullable
    op.add_column(
        "optimized_blocks",
        sa.Column(
            "optimization_run_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 3. Create a historical optimization run
    op.execute(
        """
        INSERT INTO optimization_runs (run_date, status)
        VALUES (CURRENT_TIMESTAMP, 'Historical')
        """
    )

    # 4. Assign all existing optimized blocks to that run
    op.execute(
        """
        UPDATE optimized_blocks
        SET optimization_run_id = (
            SELECT optimization_run_id
            FROM optimization_runs
            WHERE status = 'Historical'
            ORDER BY optimization_run_id DESC
            LIMIT 1
        )
        """
    )

    # 5. Make the column NOT NULL now that every existing row has a value
    op.alter_column(
        "optimized_blocks",
        "optimization_run_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # 6. Add the foreign key
    op.create_foreign_key(
        "fk_optimized_blocks_optimization_run",
        "optimized_blocks",
        "optimization_runs",
        ["optimization_run_id"],
        ["optimization_run_id"],
    )


def downgrade() -> None:
    # Remove foreign key
    op.drop_constraint(
        "fk_optimized_blocks_optimization_run",
        "optimized_blocks",
        type_="foreignkey",
    )

    # Remove column
    op.drop_column(
        "optimized_blocks",
        "optimization_run_id",
    )

    # Remove optimization runs table
    op.drop_table(
        "optimization_runs",
    )