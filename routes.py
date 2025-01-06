from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from replit import db as replit_db
from replit import web
from models import User, SimulationSession
from app import db, socketio
from simulation import WorldSimulator
import logging
import json

main = Blueprint('main', __name__)
world_simulator = WorldSimulator()

@main.before_request
def get_current_user():
    try:
        g.user = None
        auth_user = web.auth.authenticate()
        if auth_user:
            user = User.query.filter_by(replit_id=str(auth_user.id)).first()
            if not user:
                user = User(replit_id=str(auth_user.id), username=auth_user.name)
                db.session.add(user)
                try:
                    db.session.commit()
                except Exception as e:
                    logging.error(f"Error creating user: {str(e)}")
                    db.session.rollback()
            g.user = user
    except Exception as e:
        logging.error(f"Auth error: {str(e)}")
        pass

@main.route('/')
def index():
    try:
        auth_user = web.auth.authenticate()
        if not auth_user:
            return """
                <h1>Welcome to WorldSim</h1>
                <p>Please <a href="/login">sign in with Replit</a> to continue.</p>
            """
        return render_template('simulator.html')
    except Exception as e:
        logging.error(f"Index route error: {str(e)}")
        return """
            <h1>Welcome to WorldSim</h1>
            <p>Please <a href="/login">sign in with Replit</a> to continue.</p>
        """

@main.route('/login')
def login():
    return redirect(web.auth.login_url())

@main.route('/logout')
def logout():
    return redirect(web.auth.logout_url())

@socketio.on('connect')
def handle_connect():
    try:
        auth_user = web.auth.authenticate()
        if not auth_user:
            return False
        logging.debug(f'Client connected: {auth_user.name}')
        return True
    except Exception as e:
        logging.error(f"Socket connect error: {str(e)}")
        return False

@socketio.on('simulate')
def handle_simulation(message):
    try:
        auth_user = web.auth.authenticate()
        if not auth_user:
            socketio.emit('simulation_error', {'error': 'Authentication required'})
            return
    except Exception as e:
        logging.error(f"Simulation auth error: {str(e)}")
        socketio.emit('simulation_error', {'error': 'Authentication required'})
        return

    try:
        response = world_simulator.process_input(message['input'])
        logging.debug(f"Simulation response: {response}")
        socketio.emit('simulation_response', {'response': response})
    except Exception as e:
        logging.error(f'Simulation error: {str(e)}')
        socketio.emit('simulation_error', {'error': 'Simulation processing failed'})