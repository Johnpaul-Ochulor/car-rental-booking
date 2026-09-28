from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.admin import admin_bp
from app.utils import admin_required, save_uploaded_file
from app.extensions import db
from app.models import User, Booking, Subscriber, ContactQuery, Testimonial, PageContent, VehicleBrand, Vehicle
from app.vehicles.forms import VehicleBrandForm, VehicleForm


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    counts = {
        "users": User.query.count(),
        "bookings": Booking.query.count(),
        "subscribers": Subscriber.query.count(),
        "open_queries": ContactQuery.query.filter_by(is_resolved=False).count(),
    }
    return render_template("admin/dashboard.html", counts=counts)


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f"{user.name} is now {'active' if user.is_active else 'deactivated'}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/page-content")
@login_required
@admin_required
def page_content():
    pages = PageContent.query.all()
    return render_template("admin/page_content.html", pages=pages)


@admin_bp.route("/page-content/<int:page_id>/edit", methods=["POST"])
@login_required
@admin_required
def edit_page_content(page_id):
    page = PageContent.query.get_or_404(page_id)
    page.content = request.form.get("content", "")
    db.session.commit()
    flash(f"'{page.page_key}' page updated.", "success")
    return redirect(url_for("admin.page_content"))


@admin_bp.route("/testimonials")
@login_required
@admin_required
def testimonials():
    all_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template("admin/testimonials.html", testimonials=all_testimonials)


@admin_bp.route("/testimonials/<int:testimonial_id>/toggle", methods=["POST"])
@login_required
@admin_required
def toggle_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    testimonial.status = "inactive" if testimonial.status == "active" else "active"
    db.session.commit()
    flash("Testimonial status updated.", "success")
    return redirect(url_for("admin.testimonials"))


@admin_bp.route("/queries")
@login_required
@admin_required
def queries():
    all_queries = ContactQuery.query.order_by(ContactQuery.submitted_at.desc()).all()
    return render_template("admin/queries.html", queries=all_queries)


@admin_bp.route("/queries/<int:query_id>/resolve", methods=["POST"])
@login_required
@admin_required
def resolve_query(query_id):
    query = ContactQuery.query.get_or_404(query_id)
    query.is_resolved = True
    db.session.commit()
    flash("Query marked as resolved.", "success")
    return redirect(url_for("admin.queries"))

@admin_bp.route("/brands", methods=["GET", "POST"])
@admin_required
def manage_brands():
    form = VehicleBrandForm()
    if form.validate_on_submit():
        logo_path = save_uploaded_file(form.logo_image.data, folder="brands")
        brand = VehicleBrand(
            name=form.name.data,
            logo_image=logo_path,
            description=form.description.data
        )
        db.session.add(brand)
        db.session.commit()
        flash("Vehicle Brand added successfully!", "success")
        return redirect(url_for("admin.manage_brands"))

    brands = VehicleBrand.query.order_by(VehicleBrand.name).all()
    return render_template("admin/brands.html", form=form, brands=brands)


@admin_bp.route("/brands/edit/", methods=["GET", "POST"])
@admin_required
def edit_brand(brand_id):
    brand = VehicleBrand.query.get_or_404(brand_id)
    form = VehicleBrandForm(obj=brand)

    if form.validate_on_submit():
        brand.name = form.name.data
        brand.description = form.description.data
        if form.logo_image.data:
            brand.logo_image = save_uploaded_file(form.logo_image.data, folder="brands")

        db.session.commit()
        flash("Brand updated successfully!", "success")
        return redirect(url_for("admin.manage_brands"))

    return render_template("admin/edit_brand.html", form=form, brand=brand)


@admin_bp.route("/brands/delete/", methods=["POST"])
@admin_required
def delete_brand(brand_id):
    brand = VehicleBrand.query.get_or_404(brand_id)
    if brand.vehicles:
        flash("Cannot delete a brand that has vehicles assigned to it.", "danger")
        return redirect(url_for("admin.manage_brands"))

    db.session.delete(brand)
    db.session.commit()
    flash("Brand deleted successfully!", "success")
    return redirect(url_for("admin.manage_brands"))


# ==================== VEHICLE MANAGEMENT ====================

@admin_bp.route("/vehicles", methods=["GET", "POST"])
@admin_required
def manage_vehicles():
    form = VehicleForm()
    # Dynamic dropdown for brands
    form.brand_id.choices = [(b.id, b.name) for b in VehicleBrand.query.order_by(VehicleBrand.name).all()]

    if form.validate_on_submit():
        image_path = save_uploaded_file(form.image.data, folder="vehicles")
        vehicle = Vehicle(
            brand_id=form.brand_id.data,
            model_name=form.model_name.data,
            category=form.category.data,
            transmission=form.transmission.data,
            fuel_type=form.fuel_type.data,
            seats=form.seats.data,
            price_per_day=form.price_per_day.data,
            availability_status=form.availability_status.data,
            description=form.description.data,
            image=image_path
        )
        db.session.add(vehicle)
        db.session.commit()
        flash("Vehicle added successfully!", "success")
        return redirect(url_for("admin.manage_vehicles"))

    vehicles = Vehicle.query.order_by(Vehicle.id.desc()).all()
    return render_template("admin/vehicles.html", form=form, vehicles=vehicles)


@admin_bp.route("/vehicles/edit/", methods=["GET", "POST"])
@admin_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    form = VehicleForm(obj=vehicle)
    form.brand_id.choices = [(b.id, b.name) for b in VehicleBrand.query.order_by(VehicleBrand.name).all()]

    if form.validate_on_submit():
        vehicle.brand_id = form.brand_id.data
        vehicle.model_name = form.model_name.data
        vehicle.category = form.category.data
        vehicle.transmission = form.transmission.data
        vehicle.fuel_type = form.fuel_type.data
        vehicle.seats = form.seats.data
        vehicle.price_per_day = form.price_per_day.data
        vehicle.availability_status = form.availability_status.data
        vehicle.description = form.description.data

        if form.image.data:
            vehicle.image = save_uploaded_file(form.image.data, folder="vehicles")

        db.session.commit()
        flash("Vehicle updated successfully!", "success")
        return redirect(url_for("admin.manage_vehicles"))

    return render_template("admin/edit_vehicle.html", form=form, vehicle=vehicle)


@admin_bp.route("/vehicles/delete/", methods=["POST"])
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash("Vehicle deleted successfully!", "success")
    return redirect(url_for("admin.manage_vehicles"))