"""add content column to posts table

Revision ID: dfac52f2cb67
Revises: aecfceaebf58
Create Date: 2024-02-28 15:00:10.968245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfac52f2cb67'
down_revision: Union[str, None] = 'aecfceaebf58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
