from flask import Blueprint

bookings_bp = Blueprint(
    "bookings",
    __name__,
    template_folder="../templates/bookings"
)

from app.bookings import routes