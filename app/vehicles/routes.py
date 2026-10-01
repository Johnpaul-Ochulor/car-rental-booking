import os
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Vehicle, VehicleBrand
from app.vehicles import vehicles_bp
from app.vehicles.forms import BrandForm, VehicleForm

def save_image(file_storage, folder):
    if not file_storage:
        return None
    if isinstance(file_storage, str):
        return file_storage
    if hasattr(file_storage, 'filename') and file_storage.filename:
        filename = secure_filename(file_storage.filename)
        if not filename:
            return None
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
        os.makedirs(upload_path, exist_ok=True)
        file_storage.save(os.path.join(upload_path, filename))
        return f"uploads/{folder}/{filename}"
    return None

# ==================== PUBLIC ROUTES ====================
@vehicles_bp.route('/search')
def search_vehicle():

    search_query = request.args.get('q', '')

    vehicles = Vehicle.query.join(VehicleBrand).filter(
        (Vehicle.model_name.ilike(f"%{search_query}%")) |
        (Vehicle.category.ilike(f"%{search_query}%")) |
        (VehicleBrand.name.ilike(f"%{search_query}%"))
    ).all()


    return render_template(
        'vehicles/catalog.html',
        vehicles=vehicles,
        brands=VehicleBrand.query.all(),
        selected_brand=None,
        selected_category=None
    )
@vehicles_bp.route('/')
def catalog():
    brand_id = request.args.get('brand_id', type=int)
    category = request.args.get('category', type=str)
    search = request.args.get('search', type=str)


    query = Vehicle.query.filter_by(
        availability_status='available'
    )


    # Filter by brand
    if brand_id and brand_id != 0:
        query = query.filter_by(
            brand_id=brand_id
        )


    # Filter by category
    if category:
        query = query.filter_by(
            category=category
        )


    # Search by vehicle name
    if search:
        query = query.filter(
            Vehicle.model_name.ilike(f"%{search}%")
        )


    vehicles = query.all()

    brands = VehicleBrand.query.all()


    return render_template(
        'vehicles/catalog.html',
        vehicles=vehicles,
        brands=brands,
        selected_brand=brand_id,
        selected_category=category,
        search=search
    )
# Alias for index
index = catalog

@vehicles_bp.route('/<int:vehicle_id>')
def detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template('vehicles/detail.html', vehicle=vehicle)

# ==================== ADMIN BRAND CRUD ====================

@vehicles_bp.route('/admin/brands', methods=['GET', 'POST'])
@login_required
def manage_brands():
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('vehicles.admin_vehicles'))

    form = BrandForm()
    if form.validate_on_submit():
        logo_path = save_image(form.logo_image.data, 'brands')
        brand = VehicleBrand(name=form.name.data, description=form.description.data, logo_image=logo_path)
        db.session.add(brand)
        db.session.commit()
        flash('Brand added successfully!', 'success')
        return redirect(url_for('vehicles.manage_brands'))

    brands = VehicleBrand.query.all()
    return render_template('vehicles/brands.html', form=form, brands=brands)

@vehicles_bp.route('/admin/brands/delete/<int:brand_id>', methods=['POST'])
@login_required
def delete_brand(brand_id):
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('vehicles.catalog'))

    brand = VehicleBrand.query.get_or_404(brand_id)
    db.session.delete(brand)
    db.session.commit()
    flash('Brand deleted successfully!', 'success')
    return redirect(url_for('vehicles.manage_brands'))

# ==================== ADMIN VEHICLE CRUD ====================

@vehicles_bp.route('/admin/add', methods=['GET', 'POST'])
@vehicles_bp.route('/admin/edit/<int:vehicle_id>', methods=['GET', 'POST'])
@login_required
def manage_vehicle(vehicle_id=None):
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('vehicles.catalog'))

    vehicle = Vehicle.query.get(vehicle_id) if vehicle_id else None
    form = VehicleForm(obj=vehicle)
    form.brand_id.choices = [(b.id, b.name) for b in VehicleBrand.query.all()]

    if form.validate_on_submit():
        if not vehicle:
            vehicle = Vehicle()
            db.session.add(vehicle)

        vehicle.brand_id = form.brand_id.data
        vehicle.model_name = form.model_name.data
        vehicle.category = form.category.data
        vehicle.transmission = form.transmission.data
        vehicle.fuel_type = form.fuel_type.data
        vehicle.seats = form.seats.data
        vehicle.price_per_day = form.price_per_day.data
        vehicle.availability_status = form.availability_status.data
        vehicle.description = form.description.data

        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            saved_image = save_image(form.image.data, 'vehicles')
            if saved_image:
                vehicle.image = saved_image

        db.session.commit()
        flash('Vehicle saved successfully!', 'success')
        return redirect(url_for('vehicles.catalog'))

    return render_template('vehicles/form.html', form=form, vehicle=vehicle)
@vehicles_bp.route( '/admin/delete/<int:vehicle_id>', methods=['POST']
)
@login_required
def delete_vehicle(vehicle_id):
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('vehicles.catalog'))

    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle removed successfully!', 'success')
    return redirect(url_for('vehicles.catalog'))

@vehicles_bp.route('/manage')
@login_required
def manage_vehicles():

    if not current_user.is_admin():
        flash(
            "Unauthorized access",
            "danger"
        )
        return redirect(
            url_for('vehicles.catalog')
        )


    vehicles = Vehicle.query.all()


    return render_template(
        'vehicles/admin_vehicles.html',
        vehicles=vehicles
    )