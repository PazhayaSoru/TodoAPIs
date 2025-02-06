"""changing taskID from String to Integer

Revision ID: 2892ac56b0cc
Revises: 15c480288959
Create Date: 2025-02-06 21:37:48.780592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2892ac56b0cc'
down_revision: Union[str, None] = '15c480288959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from alembic import op
import sqlalchemy as sa

def upgrade():
    op.drop_constraint("tasks_pkey", "tasks", type_="primary")
    op.execute("ALTER TABLE tasks ALTER COLUMN id TYPE INTEGER USING id::INTEGER")
    op.create_primary_key("tasks_pkey", "tasks", ["id"])

def downgrade():
    op.drop_constraint("tasks_pkey", "tasks", type_="primary")
    op.execute("ALTER TABLE tasks ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR")
    op.create_primary_key("tasks_pkey", "tasks", ["id"])