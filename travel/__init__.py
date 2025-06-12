from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

# Create Database
db = SQLAlchemy()

def create_app():  
    # Create Web App
    app = Flask(__name__)
    app.secret_key = 'uncrackable'
    app.config['upload_folder'] = '/static/img'

    # Configure/Initialise Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travello.db'
    db.init_app(app)

    # Create Forms
    Bootstrap5(app)

    # Store Passwords
    Bcrypt(app)

    # Configure/Initialise Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Create User Loader
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))

    # Register Blueprints
    from .views import mainbp
    app.register_blueprint(mainbp)
    from .destinations import destbp
    app.register_blueprint(destbp)
    from .auth import authbp
    app.register_blueprint(authbp)

    @app.errorhandler(404)
    def handle_errors(error):
        return render_template("404.html", error=error)

    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)
    return app