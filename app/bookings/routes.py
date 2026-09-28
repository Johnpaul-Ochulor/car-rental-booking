from flask import render_template, request
from app.models import Vehicle
from app.bookings import bookings_bp




@bookings_bp.route("/create/<int:vehicle_id>", methods=["GET","POST"])
def create_booking(vehicle_id):

    vehicle = Vehicle.query.get_or_404(vehicle_id)


    if request.method == "POST":

        pickup_date = request.form.get("pickup_date")
        dropoff_date = request.form.get("dropoff_date")

        print(pickup_date)
        print(dropoff_date)


    return render_template(
        "bookings/create.html",
        vehicle=vehicle
    )