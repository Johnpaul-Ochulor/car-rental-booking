from flask import Blueprint, render_template

testimonials_bp = Blueprint("testimonials", __name__, template_folder="../templates/testimonials")


@testimonials_bp.route("/")
def index():
    return render_template("coming_soon.html", module="Testimonials (Dev 5)")