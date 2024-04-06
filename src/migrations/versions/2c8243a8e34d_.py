"""empty message

Revision ID: 2c8243a8e34d
Revises: 
Create Date: 2024-04-06 07:00:00.659845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c8243a8e34d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('direction_identity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('order_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spheres',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['order_status.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'user_id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('countPlace', sa.Integer(), nullable=False),
    sa.Column('registration_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deadline_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('customer_type', sa.Text(), nullable=False),
    sa.Column('orders_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('types_id', sa.Integer(), nullable=False),
    sa.Column('direction_identity_id', sa.Integer(), nullable=False),
    sa.Column('spheres_id', sa.Integer(), nullable=False),
    sa.Column('tags_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['direction_identity_id'], ['direction_identity.id'], ),
    sa.ForeignKeyConstraint(['orders_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['spheres_id'], ['spheres.id'], ),
    sa.ForeignKeyConstraint(['tags_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['types_id'], ['types.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connection',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('projects_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['projects_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('motivation_letters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('projects_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['projects_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('motivation_letters')
    op.drop_table('connection')
    op.drop_table('projects')
    op.drop_table('user_role')
    op.drop_table('orders')
    op.drop_table('user')
    op.drop_table('types')
    op.drop_table('tags')
    op.drop_table('spheres')
    op.drop_table('role')
    op.drop_table('order_status')
    op.drop_table('direction_identity')
    op.drop_table('comment')
    # ### end Alembic commands ###
