from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Testimonial, ContactQuery, Subscriber
from app.auth.decorators import admin_required  # Dev 1's decorator
from .forms import TestimonialForm, ContactForm, SubscribeForm

testimonials_bp = Blueprint("testimonials", __name__)


# ---------- Testimonials ----------
@testimonials_bp.route("/testimonials")
def list_testimonials():
    items = (Testimonial.query.filter_by(status="active")
             .order_by(Testimonial.created_at.desc()).all())
    return render_template("testimonials/list.html", testimonials=items)


@testimonials_bp.route("/testimonials/new", methods=["GET", "POST"])
@login_required
def submit_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        t = Testimonial(user_id=current_user.id,
                        message=form.message.data.strip(),
                        rating=form.rating.data,
                        status="active")
        db.session.add(t)
        db.session.commit()
        flash("Thanks for your testimonial!", "success")
        return redirect(url_for("testimonials.list_testimonials"))
    return render_template("testimonials/submit.html", form=form)


@testimonials_bp.route("/admin/testimonials")
@login_required
@admin_required
def admin_testimonials():
    items = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template("admin/testimonials.html", testimonials=items)


@testimonials_bp.route("/admin/testimonials/<int:tid>/toggle", methods=["POST"])
@login_required
@admin_required
def toggle_testimonial(tid):
    t = db.get_or_404(Testimonial, tid)
    t.status = "inactive" if t.status == "active" else "active"
    db.session.commit()
    flash(f"Testimonial is now {t.status}.", "info")
    return redirect(url_for("testimonials.admin_testimonials"))


# ---------- Contact Us ----------
@testimonials_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "GET" and current_user.is_authenticated:
        form.name.data = current_user.name
        form.email.data = current_user.email
    if form.validate_on_submit():
        q = ContactQuery(name=form.name.data.strip(),
                         email=form.email.data.strip().lower(),
                         message=form.message.data.strip())
        db.session.add(q)
        db.session.commit()
        flash("Message sent! We'll get back to you soon.", "success")
        return redirect(url_for("testimonials.contact"))
    return render_template("testimonials/contact.html", form=form)


@testimonials_bp.route("/admin/queries")
@login_required
@admin_required
def admin_queries():
    queries = ContactQuery.query.order_by(ContactQuery.submitted_at.desc()).all()
    return render_template("admin/queries.html", queries=queries)


@testimonials_bp.route("/admin/queries/<int:qid>/resolve", methods=["POST"])
@login_required
@admin_required
def resolve_query(qid):
    q = db.get_or_404(ContactQuery, qid)
    q.is_resolved = not q.is_resolved
    db.session.commit()
    return redirect(url_for("testimonials.admin_queries"))


# ---------- Newsletter ----------
@testimonials_bp.route("/subscribe", methods=["POST"])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if Subscriber.query.filter_by(email=email).first():
            flash("You're already subscribed.", "info")
        else:
            db.session.add(Subscriber(email=email))
            db.session.commit()
            flash("Subscribed successfully!", "success")
    else:
        flash("Please enter a valid email address.", "danger")
    return redirect(request.referrer or url_for("testimonials.list_testimonials"))


@testimonials_bp.route("/admin/subscribers")
@login_required
@admin_required
def admin_subscribers():
    subs = Subscriber.query.order_by(Subscriber.subscribed_at.desc()).all()
    return render_template("admin/subscribers.html", subscribers=subs)