from flask import Blueprint, render_template

bookings_bp = Blueprint("bookings", __name__, template_folder="../templates/bookings")


@bookings_bp.route("/")
def index():
    return render_template("coming_soon.html", module="Bookings (Dev 3 & 4)")