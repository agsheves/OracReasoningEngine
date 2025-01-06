import os
import logging
from app import create_app, socketio

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")

    if os.environ.get('FLASK_ENV') == 'production':
        logger.info("Running in production mode")
        app.run(host='0.0.0.0', port=port)
    else:
        logger.info("Running in development mode with Socket.IO support")
        socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)