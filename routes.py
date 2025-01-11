from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, SimulationSession
from app import db, socketio
import routing_and_logic
from simulation import WorldSimulator
import logging
import json

main = Blueprint('main', __name__)
world_simulator = WorldSimulator()

@main.route('/')
@login_required
def index():
    return render_template('simulator.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('main.register'))

        user = User(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        try:
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.index'))
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            db.session.rollback()
            flash('Registration failed. Please try again.')

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Admin routes for user management
@main.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@main.route('/admin/users/validate/<int:user_id>')
@login_required
def validate_user(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    user.is_validated = True
    try:
        db.session.commit()
        flash(f'User {user.username} has been validated')
    except Exception as e:
        logging.error(f"Validation error: {str(e)}")
        db.session.rollback()
        flash('Validation failed')
    return redirect(url_for('main.admin_users'))

@main.route('/admin/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot delete your own account')
        return redirect(url_for('main.admin_users'))

    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted')
    except Exception as e:
        logging.error(f"Deletion error: {str(e)}")
        db.session.rollback()
        flash('Deletion failed')
    return redirect(url_for('main.admin_users'))

@socketio.on('connect')
@login_required
def handle_connect():
    logging.debug(f'Client connected: {current_user.username}')

@socketio.on('simulate')
def handle_simulation(message):
    try:
        logging.debug(f'Processing simulation request: {message["input"]}')
        # First, process the scenario
        scenario_data = routing_and_logic.process_scenario(message['input'])

        # Emit the formatted scenario for confirmation
        socketio.emit('simulation_confirmation', {
            'scenario': scenario_data['display_format'],
            'heuristic': scenario_data['heuristic'],
            'heuristic_description': scenario_data['heuristic_description'],
            'original_prompt': message['input']  # Include original prompt for editing
        })

        # Store the parsed scenario in the session
        session = SimulationSession(
            user_id=current_user.id,
            world_state=json.dumps(scenario_data['parsed_scenario'])
        )
        db.session.add(session)
        db.session.commit()
        session.initialize_session_settings(current_user)

    except Exception as e:
        logging.error(f'Scenario processing error: {str(e)}')
        socketio.emit('simulation_error', {'error': str(e)})

@socketio.on('confirm_simulation')
def handle_simulation_confirmation(confirmed):
    try:
        if confirmed:
            # Get the latest session for the user
            session = SimulationSession.query.filter_by(
                user_id=current_user.id
            ).order_by(SimulationSession.started_at.desc()).first()

            if not session:
                raise ValueError("No active simulation session found")

            # Initaize the world simulator with the base scenario
            scenario = json.loads(session.world_state)
            response = world_simulator.initialize_simulation(json.dumps(scenario))
            socketio.emit('simulation_response', {'response': response})
        else:
            socketio.emit('simulation_cancelled', {'message': 'Simulation cancelled by user'})

    except Exception as e:
        logging.error(f'Simulation error: {str(e)}')
        socketio.emit('simulation_error', {'error': str(e)})