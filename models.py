from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_validated = db.Column(db.Boolean, default=False)
    user_settings = db.Column(db.JSON, default=lambda: {
        'theme': 'dark',
        'language': 'en',
        'notifications_enabled': True,
        'auto_save': True,
        'display_format': 'detailed',
        'simulation_mode': 'standard'
    })

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SimulationSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    world_state = db.Column(db.Text)
    session_settings = db.Column(db.JSON, default=lambda: {})

    def initialize_session_settings(self, user):
        self.session_settings = user.user_settings.copy()
        db.session.commit()