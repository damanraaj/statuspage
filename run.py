from flask import Flask
from app import create_app, db
from app.models import User, Service, Incident, IncidentUpdate, ScheduledMaintenance
import app.events  # Import the events module

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Service': Service,
        'Incident': Incident,
        'IncidentUpdate': IncidentUpdate,
        'ScheduledMaintenance': ScheduledMaintenance
    }

if __name__ == '__main__':
    from app import socketio
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)