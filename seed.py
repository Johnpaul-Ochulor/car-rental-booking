from app import create_app
from app.extensions import db
from app.models import User, Subscriber, ContactQuery, Testimonial

app = create_app()

with app.app_context():
    if not User.query.filter_by(email="admin@fastcars.com").first():
        admin = User(name="Admin", email="admin@fastcars.com", role="admin")
        admin.set_password("Admin123!")
        db.session.add(admin)

    db.session.add(Subscriber(email="test1@example.com"))
    db.session.add(ContactQuery(name="John Doe", email="john@example.com", message="Do you rent SUVs?"))

    db.session.commit()
    print("Seed complete. Login with admin@fastcars.com / Admin123!")