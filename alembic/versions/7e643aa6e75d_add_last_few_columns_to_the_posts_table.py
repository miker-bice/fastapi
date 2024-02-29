"""add last few columns to the posts table

Revision ID: 7e643aa6e75d
Revises: 4e4fd5475325
Create Date: 2024-02-28 15:53:12.833431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e643aa6e75d'
down_revision: Union[str, None] = '4e4fd5475325'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('is_published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "created_at")
    pass
