from flask import Blueprint, render_template, redirect, url_for, g
from replit import web
from models import User, SimulationSession
from app import db, socketio
from simulation import WorldSimulator
import logging
import json

main = Blueprint('main', __name__)
world_simulator = WorldSimulator()

@main.before_app_request
def get_current_user():
    g.user = None
    try:
        auth_user = web.Auth.get_current_user()
        if auth_user:
            user = User.query.filter_by(replit_id=str(auth_user.id)).first()
            if not user:
                user = User(replit_id=str(auth_user.id), username=auth_user.name)
                db.session.add(user)
                db.session.commit()
            g.user = user
    except Exception as e:
        logging.error(f"Auth error: {str(e)}")

@main.route('/')
def index():
    if not g.user:
        return render_template('login.html')
    return render_template('simulator.html')

@main.route('/login')
def login():
    return redirect(web.auth.login_url())

@main.route('/logout')
def logout():
    return redirect(web.auth.logout_url())

@socketio.on('connect')
def handle_connect():
    if not g.user:
        return False
    logging.debug(f'Client connected: {g.user.username}')
    return True

@socketio.on('simulate')
def handle_simulation(message):
    if not g.user:
        socketio.emit('simulation_error', {'error': 'Authentication required'})
        return

    try:
        response = world_simulator.process_input(message['input'])
        logging.debug(f"Simulation response: {response}")
        socketio.emit('simulation_response', {'response': response})
    except Exception as e:
        logging.error(f'Simulation error: {str(e)}')
        socketio.emit('simulation_error', {'error': 'Simulation processing failed'})