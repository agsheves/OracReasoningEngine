
from app import db
from models import User, SimulationSession
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add conversation_history column
    op.add_column('simulation_session', 
                  sa.Column('conversation_history', sa.Text, nullable=True, default='[]'))

def downgrade():
    # Remove conversation_history column if needed
    op.drop_column('simulation_session', 'conversation_history')
