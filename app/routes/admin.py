from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Service, Incident, IncidentUpdate
from app import db
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('admin/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@bp.route('/')
@login_required
def dashboard():
    services = Service.query.all()
    incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', services=services, incidents=incidents)

@bp.route('/services', methods=['GET', 'POST'])
@login_required
def services():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        service = Service(name=name, description=description, status='operational')
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully', 'success')
        return redirect(url_for('admin.services'))
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@bp.route('/service/<int:service_id>/status', methods=['POST'])
@login_required
def update_service_status(service_id):
    service = Service.query.get_or_404(service_id)
    status = request.form.get('status')
    if status in ['operational', 'degraded', 'outage']:
        service.status = status
        db.session.commit()
        flash(f'Service status updated to {status}', 'success')
    return redirect(url_for('admin.services'))

@bp.route('/incidents', methods=['GET', 'POST'])
@login_required
def incidents():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        title = request.form.get('title')
        description = request.form.get('description')
        incident = Incident(
            service_id=service_id,
            title=title,
            description=description,
            status='investigating'
        )
        db.session.add(incident)
        db.session.commit()
        flash('Incident created successfully', 'success')
        return redirect(url_for('admin.incidents'))
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    services = Service.query.all()
    return render_template('admin/incidents.html', incidents=incidents, services=services)

@bp.route('/incident/<int:incident_id>/status', methods=['POST'])
@login_required
def update_incident_status(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    status = request.form.get('status')
    if status in ['investigating', 'identified', 'monitoring', 'resolved']:
        incident.status = status
        incident.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Incident status updated to {status}', 'success')
    return redirect(url_for('admin.incidents'))

@bp.route('/incident/<int:incident_id>/update', methods=['POST'])
@login_required
def add_incident_update(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    message = request.form.get('message')
    if message:
        update = IncidentUpdate(
            incident_id=incident_id,
            message=message,
            status=incident.status
        )
        db.session.add(update)
        db.session.commit()
        flash('Update added successfully', 'success')
    return redirect(url_for('admin.incidents'))
