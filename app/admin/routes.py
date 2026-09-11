from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.admin import admin_bp
from app.utils import admin_required
from app.extensions import db
from app.models import User, Booking, Subscriber, ContactQuery, Testimonial, PageContent


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