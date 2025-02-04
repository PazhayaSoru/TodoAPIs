"""initial setup

Revision ID: a387cd922540
Revises: 
Create Date: 2025-02-04 23:13:35.271600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a387cd922540'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id",sa.Integer,nullable=False,primary_key=True))


def downgrade() -> None:
    op.drop_table("users")
