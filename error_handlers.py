# error_handlers.py
# Handles the error handlers for the web app

from flask import render_template
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        logger.info(f"Page not found: {error}")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Server Error: {error}")
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        logger.warning(f"Forbidden access: {error}")
        return render_template("errors/403.html"), 403

    @app.errorhandler(401)
    def unauthorized_error(error):
        logger.warning(f"Unauthorized access: {error}")
        return render_template("errors/401.html"), 401
