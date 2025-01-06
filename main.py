from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    import os
    if os.environ.get('FLASK_ENV') == 'production':
        # In production, Gunicorn will handle the app directly
        # Use app.run() directly as gunicorn will manage workers
        app.run()
    else:
        # In development, use socketio.run with debug mode
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)