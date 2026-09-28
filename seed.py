from app import create_app
from app.extensions import db
from app.models import User, Subscriber, ContactQuery, Testimonial
from app.models import VehicleBrand, Vehicle


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



with app.app_context():

    toyota = VehicleBrand.query.filter_by(name="Toyota").first()

    if not toyota:
        toyota = VehicleBrand(
            name="Toyota",
            description="Reliable Japanese vehicles"
        )
        db.session.add(toyota)


    bmw = VehicleBrand.query.filter_by(name="BMW").first()

    if not bmw:
        bmw = VehicleBrand(
            name="BMW",
            description="Luxury German vehicles"
        )
        db.session.add(bmw)


    mercedes = VehicleBrand.query.filter_by(name="Mercedes Benz").first()

    if not mercedes:
        mercedes = VehicleBrand(
            name="Mercedes Benz",
            description="Premium vehicles"
        )
        db.session.add(mercedes)


    db.session.commit()



    existing_vehicle = Vehicle.query.first()

    if not existing_vehicle:

        cars = [

            Vehicle(
                brand_id=toyota.id,
                model_name="Camry 2025",
                category="Sedan",
                transmission="Automatic",
                fuel_type="Petrol",
                seats=5,
                price_per_day=50000,
                availability_status="available",
                description="Comfortable sedan suitable for business and family trips."
            ),


            Vehicle(
                brand_id=bmw.id,
                model_name="BMW X5",
                category="SUV",
                transmission="Automatic",
                fuel_type="Petrol",
                seats=7,
                price_per_day=120000,
                availability_status="available",
                description="Luxury SUV with premium interior and powerful performance."
            ),


            Vehicle(
                brand_id=mercedes.id,
                model_name="Mercedes C-Class",
                category="Sedan",
                transmission="Automatic",
                fuel_type="Hybrid",
                seats=5,
                price_per_day=100000,
                availability_status="available",
                description="Executive vehicle designed for comfort."
            )

        ]


        db.session.add_all(cars)

        db.session.commit()


print("Vehicle seed completed")