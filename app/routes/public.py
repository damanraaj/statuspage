from flask import Blueprint, render_template
from app.models import Service, Incident, ScheduledMaintenance, IncidentUpdate
from datetime import datetime, timedelta

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    services = Service.query.all()
    current_time = datetime.utcnow()
    
    # Get active incidents
    active_incidents = Incident.query.filter(
        Incident.status.in_(['investigating', 'identified', 'monitoring'])
    ).order_by(Incident.created_at.desc()).all()
    
    # Get maintenance events
    maintenance_events = ScheduledMaintenance.query.filter(
        ScheduledMaintenance.end_time >= current_time
    ).order_by(ScheduledMaintenance.start_time.asc()).all()
    
    # Get recent timeline events (last 30 days)
    thirty_days_ago = current_time - timedelta(days=30)
    
    # Get recent incidents and their updates
    recent_incidents = Incident.query.filter(
        Incident.created_at >= thirty_days_ago
    ).order_by(Incident.created_at.desc()).all()
    
    recent_updates = IncidentUpdate.query.join(Incident).filter(
        IncidentUpdate.created_at >= thirty_days_ago
    ).order_by(IncidentUpdate.created_at.desc()).all()
    
    # Combine all events into a timeline
    timeline_events = []
    
    # Add incidents
    for incident in recent_incidents:
        timeline_events.append({
            'type': 'incident',
            'event': incident,
            'timestamp': incident.created_at,
            'title': incident.title,
            'status': incident.status,
            'description': incident.description
        })
    
    # Add incident updates
    for update in recent_updates:
        timeline_events.append({
            'type': 'update',
            'event': update,
            'timestamp': update.created_at,
            'title': f"Update: {update.incident.title}",
            'status': update.status,
            'description': update.message
        })
    
    # Add maintenance events
    recent_maintenance = ScheduledMaintenance.query.filter(
        (ScheduledMaintenance.start_time >= thirty_days_ago) |
        (ScheduledMaintenance.end_time >= thirty_days_ago)
    ).all()
    
    for maintenance in recent_maintenance:
        timeline_events.append({
            'type': 'maintenance',
            'event': maintenance,
            'timestamp': maintenance.start_time,
            'title': maintenance.title,
            'status': maintenance.status,
            'description': maintenance.description
        })
    
    # Sort timeline events by timestamp, most recent first
    timeline_events.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('public/index.html',
                         services=services,
                         active_incidents=active_incidents,
                         maintenance_events=maintenance_events,
                         timeline_events=timeline_events)

@bp.route('/history')
def history():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('public/history.html', incidents=incidents)
