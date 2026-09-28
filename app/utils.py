import os
import uuid
from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename


def admin_required(view_func):
    """Decorator to ensure only admin users can access a route."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return view_func(*args, **kwargs)
    return wrapped


def save_uploaded_file(file_storage, folder="vehicles"):
    """
    Saves an uploaded image in app/static/uploads//
    and returns its path for database storage.
    """
    if not file_storage or not file_storage.filename:
        return None

    # Sanitize and assign a unique filename to avoid overwrites
    original_filename = secure_filename(file_storage.filename)
    extension = os.path.splitext(original_filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{extension}"

    # Build folder directory: app/static/uploads//
    upload_folder = os.path.join(current_app.root_path, "static", "uploads", folder)
    os.makedirs(upload_folder, exist_ok=True)

    # Save file to disk
    file_path = os.path.join(upload_folder, unique_filename)
    file_storage.save(file_path)

    # Return relative path (e.g. 'uploads/vehicles/a1b2c3d4.jpg')
    return f"uploads/{folder}/{unique_filename}"