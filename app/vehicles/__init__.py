from flask import Blueprint, render_template

vehicles_bp = Blueprint("vehicles", __name__, template_folder="../templates/vehicles")


@vehicles_bp.route("/")
def index():
    return render_template("coming_soon.html", module="Vehicles (Dev 2)")