from flask import Flask,redirect,url_for
from app.extensions import db, login_manager, migrate
from app.models import User
import click
from flask_mail import Mail, Message


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    migrate.init_app(app, db)

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def index():
        return redirect(url_for('auth.index'))
    
    
    @app.cli.command('create-admin')
    @click.argument('name')
    @click.argument('email')
    @click.argument('phone')
    @click.argument('password')
    def create_admin(name, email, phone, password):
        """Creates a new admin user."""
        user = User.query.filter_by(email=email).first()
        if user:
            click.echo('Error: Email already exists.')
            return

        admin = User(
            name=name,
            email=email,
            phone=phone,
            role='admin'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        click.echo(f'Admin account created for {email}!')
    
    mail.init_app(app)


    return app