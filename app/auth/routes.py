from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import csrf
auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates/auth"
)
# @csrf.exempt
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    print("LOGIN FUNCTION RUNNING")

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        print("EMAIL:", email)
        print("PASSWORD:", password)

        session["user"] = {
            "email": email,
            "role": "customer"
        }

        return redirect(url_for("vehicles.catalog"))

    return render_template("login.html")