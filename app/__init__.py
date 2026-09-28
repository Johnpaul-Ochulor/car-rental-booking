from flask import Flask, render_template
from app.extensions import db, login_manager, migrate, csrf
from app.models import User, Vehicle, VehicleBrand


def create_app():

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



    from app.models import User


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


    return app