from app import create_app, db
from app.models import User, Service, Incident, IncidentUpdate, ScheduledMaintenance

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
    app.run(debug=True)