from flask import Blueprint, render_template
from app.models import Service, Incident

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    services = Service.query.all()
    active_incidents = Incident.query.filter(
        Incident.status != 'resolved'
    ).order_by(Incident.created_at.desc()).all()
    return render_template('public/index.html', services=services, active_incidents=active_incidents)

@bp.route('/history')
def history():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('public/history.html', incidents=incidents)
