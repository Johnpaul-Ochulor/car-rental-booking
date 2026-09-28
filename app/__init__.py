<<<<<<< HEAD
from flask import Flask, render_template
from app.extensions import db, login_manager, migrate, csrf
from app.models import User, Vehicle, VehicleBrand
=======
import click
from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from app.extensions import db, login_manager, migrate
from app.models import User
>>>>>>> origin/dev1-auth

mail = Mail()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
<<<<<<< HEAD

    from app.bookings import bookings_bp
    app = Flask(
        __name__,
        instance_relative_config=True
    )


    app.config.from_pyfile("config.py")


    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)


=======
    # 1. Instantiate Flask App First
    app = Flask(__name__)

    # 2. Load Configuration Settings
    app.config.from_pyfile('../instance/config.py', silent=True)
    
    # Fallback/Default Mail Configuration (Overridden by instance/config.py if present)
    app.config.setdefault('MAIL_SERVER', 'smtp.gmail.com')
    app.config.setdefault('MAIL_PORT', 465)
    app.config.setdefault('MAIL_USE_TLS', False)
    app.config.setdefault('MAIL_USE_SSL', True)
    app.config.setdefault('MAIL_USERNAME', 'johnajibolz12345@gmail.com')
    app.config.setdefault('MAIL_PASSWORD', 'tqiwxmfthyaemvbx')
    app.config.setdefault('MAIL_DEFAULT_SENDER', 'johnajibolz12345@gmail.com')

    # 3. Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)  # Initialized AFTER setting configs
>>>>>>> origin/dev1-auth

    # 4. Register Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.testimonials.routes import testimonials_bp
    app.register_blueprint(testimonials_bp)

<<<<<<< HEAD

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))



    from app.auth import auth_bp
    from app.vehicles import vehicles_bp
    from app.bookings import bookings_bp
    from app.testimonials import testimonials_bp
    from app.admin import admin_bp



    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        vehicles_bp,
        url_prefix="/vehicles"
    )



    app.register_blueprint(
    bookings_bp,
    url_prefix="/bookings"
)


    app.register_blueprint(
        testimonials_bp,
        url_prefix="/testimonials"
    )


    app.register_blueprint(
        admin_bp,
        url_prefix="/admin"
    )



    @app.route("/")
    def home():

        vehicles = Vehicle.query.filter_by(
            availability_status="available"
        ).limit(4).all()


        return render_template(
            "landing.html",
            vehicles=vehicles
        )

=======
    # 5. Root Route
    @app.route('/')
    def index():
        return redirect(url_for('auth.index'))

    # 6. CLI Commands
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
>>>>>>> origin/dev1-auth

    return app