import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

    # ----- НАСТРОЙКА БАЗЫ ДАННЫХ (поддержка PostgreSQL и SQLite) -----
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        # Render использует 'postgres://', но SQLAlchemy 1.4+ требует 'postgresql://'
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Локальный режим: SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # ----------------------------------------------------------------

    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from . import routes, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(api.bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))