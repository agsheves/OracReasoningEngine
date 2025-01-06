import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
# Initialize SocketIO with proper CORS and error handling
socketio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

def create_app():
    logger.info("Initializing Flask application...")
    app = Flask(__name__)

    # Environment-based configuration
    is_production = os.environ.get('FLASK_ENV') == 'production'
    logger.info(f"Running in {'production' if is_production else 'development'} mode")

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev_key_replace_in_production")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Production specific configuration
    if is_production:
        app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='Lax',
            PERMANENT_SESSION_LIFETIME=3600,  # 1 hour
            DEBUG=False
        )
        logger.info("Production configuration applied")
    else:
        app.config['DEBUG'] = True
        logger.info("Development configuration applied")

    # Initialize extensions
    logger.info("Initializing Flask extensions...")
    db.init_app(app)
    socketio.init_app(app, async_mode='eventlet', logger=True, engineio_logger=True)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    with app.app_context():
        logger.info("Setting up application context...")
        # Import parts of our application
        from models import User
        db.create_all()
        logger.info("Database tables created")

        # Register blueprints
        from routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
        logger.info("Blueprints registered")

        # Register error handlers
        from error_handlers import register_error_handlers
        register_error_handlers(app)
        logger.info("Error handlers registered")

        return app