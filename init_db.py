from app import create_app, db
from app.models import User, Service
import os

def init_db():
    app = create_app()
    with app.app_context():
        # Create database tables
        db.create_all()

        # Check if admin user exists
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            # Create admin user
            admin = User(
                email=admin_email,
                is_admin=True
            )
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)

            # Create some initial services
            services = [
                Service(
                    name='Website',
                    description='Main company website',
                    status='operational'
                ),
                Service(
                    name='API',
                    description='REST API endpoints',
                    status='operational'
                ),
                Service(
                    name='Database',
                    description='Main database service',
                    status='operational'
                )
            ]
            for service in services:
                db.session.add(service)

            db.session.commit()
            print("Database initialized with admin user and initial services.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
