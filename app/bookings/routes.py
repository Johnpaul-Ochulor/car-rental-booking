# from datetime import datetime
# from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from app.models import Vehicle, Booking
# from app.extensions import db
# from app.bookings import bookings_bp


# @bookings_bp.route("/")
# @login_required
# def index():
#     user_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.id.desc()).all()
#     return render_template("bookings/index.html", bookings=user_bookings)


# @bookings_bp.route("/create/", methods=["GET", "POST"])
# @bookings_bp.route("/create/", methods=["GET", "POST"])
# @login_required
# def create_booking(vehicle_id=None):
#     # Support both URL parameter (/create/3) and query string (/create/?vehicle_id=3)
#     if vehicle_id is None:
#         vehicle_id = request.args.get("vehicle_id", type=int)

#     if not vehicle_id:
#         flash("Vehicle not selected.", "warning")
#         return redirect(url_for("vehicles.catalog"))

#     vehicle = Vehicle.query.get_or_404(vehicle_id)

#     if request.method == "POST":
#         pickup_date_str = request.form.get("pickup_date")
#         dropoff_date_str = request.form.get("dropoff_date")

#         if not pickup_date_str or not dropoff_date_str:
#             flash("Please enter both pickup and dropoff dates.", "danger")
#             return render_template("bookings/create.html", vehicle=vehicle)

#         # Parse string dates into datetime.date objects
#         pickup_date = datetime.strptime(pickup_date_str, "%Y-%m-%d").date()
#         return_date = datetime.strptime(dropoff_date_str, "%Y-%m-%d").date()

#         # Calculate duration and total cost
#         rental_days = (return_date - pickup_date).days
#         if rental_days <= 0:
#             rental_days = 1

#         total_price = (rental_days * float(vehicle.price_per_day)) + 85.0

#         new_booking = Booking(
#             user_id=current_user.id,
#             vehicle_id=vehicle.id,
#             pickup_date=pickup_date,
#             return_date=return_date,
#             total_price=total_price,
#             status="Confirmed"
#         )

#         db.session.add(new_booking)
#         db.session.commit()

#         flash("Booking reserved successfully!", "success")
#         return redirect(url_for("bookings.index"))

#     return render_template("bookings/create.html", vehicle=vehicle)


# from datetime import datetime
# from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from app.models import Vehicle, Booking
# from app.extensions import db
# from app.bookings import bookings_bp

import os
import secrets
from datetime import date, datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_mailman import EmailMessage
import requests

from app.bookings import bookings_bp
from app.extensions import db
from app.models import Booking, Payment, Vehicle


def generate_booking_reference(prefix: str = "BK-LGNGN") -> str:
    default_charset = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
    date_part = datetime.now().strftime("%y%m%d")  # YYMMDD
    random_part = "".join(secrets.choice(default_charset) for _ in range(8))
    return f"{prefix}-{date_part}-{random_part}"


def paystack_init(paystack_data: dict) -> requests.Response:
    secret_key = os.environ.get("PAYSTACK_SECRET_KEY")
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }

    return requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=paystack_data,
        headers=headers,
        timeout=10,
    )


def send_email(subject, body, reciepient):
    try:
        msg = EmailMessage(
            subject=subject,
            body=body,
            to=reciepient,
        )
        msg.send()
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


@bookings_bp.route("/create/<int:vehicle_id>", methods=["GET"])
@login_required
def create_booking(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template("bookings/create.html", vehicle=vehicle)


@bookings_bp.route("/book/<int:vehicle_id>", methods=["POST"])
@login_required
def submit_booking(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    pickup_date_str = request.form.get("pickup_date")
    dropoff_date_str = request.form.get("dropoff_date")
    location = request.form.get("location")
    terms = request.form.get("terms")
    current_date = date.today()

    if not pickup_date_str or not dropoff_date_str or not location:
        flash("Pickup date, drop-off date, and location are required.", "danger")
        return render_template("bookings/create.html", vehicle=vehicle)

    if not terms:
        flash("You must agree to the Terms & Conditions before completing your booking.", "warning")
        return render_template("bookings/create.html", vehicle=vehicle)

    try:
        pickup_date = datetime.strptime(pickup_date_str, "%Y-%m-%d").date()
        dropoff_date = datetime.strptime(dropoff_date_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format provided.", "danger")
        return render_template("bookings/create.html", vehicle=vehicle)

    if dropoff_date <= pickup_date:
        flash("Drop-off date must be after pickup date.", "danger")
        return render_template("bookings/create.html", vehicle=vehicle)

    if pickup_date < current_date:
        flash("Pickup date cannot be in the past.", "danger")
        return render_template("bookings/create.html", vehicle=vehicle)

    try:
        # Lock the vehicle row to prevent concurrent double-booking
        vehicle_locked = Vehicle.query.with_for_update().get(vehicle_id)

        # Check for date overlaps across all bookings for this vehicle
        overlapping_booking = Booking.query.filter(
            Booking.vehicle_id == vehicle_locked.id,
            Booking.pickup_date < dropoff_date,
            Booking.return_date > pickup_date,
            Booking.status.in_({"pending", "confirmed"}),
        ).first()

        if overlapping_booking:
            flash("Vehicle is already booked for the selected date range.", "warning")
            return render_template("bookings/create.html", vehicle=vehicle)

        no_of_days = (dropoff_date - pickup_date).days
        rate = vehicle_locked.price_per_day
        tax = 85

        booking_ref = generate_booking_reference()
        total = (no_of_days * rate) + tax

        new_booking = Booking(
            user_id=current_user.id,
            vehicle_id=vehicle_locked.id,
            pickup_date=pickup_date,
            return_date=dropoff_date,
            pickup_location=location,
            total_price=total,
            reference=booking_ref,
            status="pending",
        )
        db.session.add(new_booking)
        db.session.flush()

        payment_amount = int(total * 100)
        new_payment = Payment(
            booking_id=new_booking.id,
            booking_reference=new_booking.reference,
            customer_id=current_user.id,
            reference=None,
            amount=payment_amount,
            status="pending",
        )
        db.session.add(new_payment)
        db.session.flush()

        paystack_data = {
            "email": current_user.email,
            "amount": payment_amount,  # Paystack expects amounts in kobo/cents
            "reference": new_booking.reference,
            "callback_url": url_for("bookings.paystack_verify", _external=True),
            "metadata": {
                "booking_id": new_booking.id,
                "payment_id": new_payment.id,
                "user_id": current_user.id,
            },
        }

        response = paystack_init(paystack_data)
        res_data = response.json()

        if response.status_code == 200 and res_data.get("status"):
            db.session.commit()
            print("after db commit")
            url = res_data["data"]["authorization_url"]
            return redirect(url)

        # Rollback DB changes if Paystack initialization fails
        db.session.rollback()
        flash("Failed to initialize payment with Paystack. Please try again.", "danger")
        return render_template("bookings/create.html", vehicle=vehicle)

    except Exception as e:
        db.session.rollback()
        print("BOOKING ERROR")
        print(repr(e))
        import traceback

        traceback.print_exc()

        flash("An error occurred processing your request. Please try again.", "danger")
        return render_template("bookings/create.html", vehicle=vehicle)


@bookings_bp.route("/verify-payment", methods=["GET"])
@login_required
def paystack_verify():
    reference = request.args.get("reference")

    if not reference:
        flash("No transaction reference provided.", "danger")
        return redirect(url_for("bookings.user_bookings"))

    secret_key = os.environ.get("PAYSTACK_SECRET_KEY")
    headers = {"Authorization": f"Bearer {secret_key}"}
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"

    try:
        response = requests.get(verify_url, headers=headers, timeout=10)
        res_data = response.json()

        if (
            response.status_code == 200
            and res_data.get("data", {}).get("status") == "success"
        ):
            paystack_data = res_data["data"]
            meta = paystack_data.get("metadata", {})
            booking_id = meta.get("booking_id")
            payment_id = meta.get("payment_id")
            paystack_reference = paystack_data.get("reference")

            booking = Booking.query.get(booking_id)
            payment = Payment.query.get(payment_id)
            vehicle = Vehicle.query.get(booking.vehicle_id)

            # Validate amount paid matches expected payment amount (in kobo/cents)
            expected_amount = payment.amount if payment else 0
            if booking and payment and paystack_data.get("amount") == expected_amount:
                booking.status = "confirmed"
                payment.status = "success"
                payment.reference = paystack_reference
                payment.paid_at = datetime.now()
                db.session.commit()

                email_body = f"""
Dear {current_user.name},

Your booking has been successfully confirmed!

Booking Summary:
----------------
• Booking Reference: {booking.reference}
• Vehicle: {vehicle.model_name} {vehicle.category}
• Pickup Location: {booking.pickup_location}
• Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
• Return Date: {booking.return_date.strftime('%B %d, %Y')}
• Total Amount Paid: ₦{booking.total_price:,.2f}

Thank you for choosing us!

Best regards,
The Management Team
"""
                is_email_sent = send_email(
                    subject="Fast Cars Booking Confirmation",
                    body=email_body,
                    reciepient=[current_user.email],
                )

                flash("Payment successful! Your booking is confirmed.", "success")
                return redirect(url_for("bookings.user_bookings"))

    except requests.RequestException as e:
        print(f"an error occured: {str(e)}")
        booking.status = "cancelled"
        payment.status = "failed"

    flash("Payment verification failed or was cancelled.", "danger")
    return redirect(url_for("bookings.user_bookings"))


@bookings_bp.route("/user_all", methods=["GET"])
@login_required
def user_bookings():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    for user_booking in user_bookings:
        vehicle = Vehicle.query.get_or_404(user_booking.vehicle_id)
        if vehicle:
            user_booking.vehicle_name = vehicle.model_name
            user_booking.vehicle_category = vehicle.category
    return render_template("bookings/index.html", bookings=user_bookings)


@bookings_bp.route("/admin_all", methods=["GET"])
@login_required
def all_bookings():
    bookings = Booking.query.all()
    for booking in bookings:
        vehicle = Vehicle.query.get_or_404(booking.vehicle_id)
        if vehicle:
            booking.vehicle_name = vehicle.model_name
            booking.vehicle_category = vehicle.category
    return render_template("bookings/index.html", bookings=bookings)


@bookings_bp.route("/completed", methods=["POST"])
@login_required
def booking_completed():
    pass
