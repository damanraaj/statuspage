from flask import Blueprint, render_template
from app.models import Service, Incident, ScheduledMaintenance
from datetime import datetime

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    services = Service.query.all()
    active_incidents = Incident.query.filter(
        Incident.status.in_(['investigating', 'identified', 'monitoring'])
    ).order_by(Incident.created_at.desc()).all()
    
    # Get ongoing and upcoming maintenance events
    current_time = datetime.utcnow()
    maintenance_events = ScheduledMaintenance.query.filter(
        ScheduledMaintenance.end_time >= current_time
    ).order_by(ScheduledMaintenance.start_time.asc()).all()
    
    return render_template('public/index.html', 
                         services=services, 
                         active_incidents=active_incidents,
                         maintenance_events=maintenance_events)

@bp.route('/history')
def history():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('public/history.html', incidents=incidents)
