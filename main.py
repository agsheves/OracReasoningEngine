
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    import os
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=5000)
    else:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
