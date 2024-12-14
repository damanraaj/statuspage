from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'

    # Add context processor for current year
    @app.context_processor
    def inject_year():
        return {'current_year': datetime.utcnow().year}

    from app.routes import admin, public
    app.register_blueprint(admin.bp)
    app.register_blueprint(public.bp)

    return app
