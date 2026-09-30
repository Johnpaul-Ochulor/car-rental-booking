from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Vehicle, Booking
from app.extensions import db
from app.bookings import bookings_bp


@bookings_bp.route("/")
@login_required
def index():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.id.desc()).all()
    return render_template("bookings/index.html", bookings=user_bookings)


@bookings_bp.route("/create/", methods=["GET", "POST"])
@bookings_bp.route("/create/", methods=["GET", "POST"])
@login_required
def create_booking(vehicle_id=None):
    # Support both URL parameter (/create/3) and query string (/create/?vehicle_id=3)
    if vehicle_id is None:
        vehicle_id = request.args.get("vehicle_id", type=int)

    if not vehicle_id:
        flash("Vehicle not selected.", "warning")
        return redirect(url_for("vehicles.catalog"))

    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        pickup_date_str = request.form.get("pickup_date")
        dropoff_date_str = request.form.get("dropoff_date")

        if not pickup_date_str or not dropoff_date_str:
            flash("Please enter both pickup and dropoff dates.", "danger")
            return render_template("bookings/create.html", vehicle=vehicle)

        # Parse string dates into datetime.date objects
        pickup_date = datetime.strptime(pickup_date_str, "%Y-%m-%d").date()
        return_date = datetime.strptime(dropoff_date_str, "%Y-%m-%d").date()

        # Calculate duration and total cost
        rental_days = (return_date - pickup_date).days
        if rental_days <= 0:
            rental_days = 1

        total_price = (rental_days * float(vehicle.price_per_day)) + 85.0

        new_booking = Booking(
            user_id=current_user.id,
            vehicle_id=vehicle.id,
            pickup_date=pickup_date,
            return_date=return_date,
            total_price=total_price,
            status="Confirmed"
        )

        db.session.add(new_booking)
        db.session.commit()

        flash("Booking reserved successfully!", "success")
        return redirect(url_for("bookings.index"))

    return render_template("bookings/create.html", vehicle=vehicle)