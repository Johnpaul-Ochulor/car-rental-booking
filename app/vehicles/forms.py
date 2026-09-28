from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class BrandForm(FlaskForm):
    name = StringField('Brand Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    logo_image = FileField('Brand Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])
    submit = SubmitField('Save Brand')

# Alias so Dev 6 (Admin module) imports don't break
VehicleBrandForm = BrandForm

class VehicleForm(FlaskForm):
    brand_id = SelectField('Brand', coerce=int, validators=[DataRequired()])
    model_name = StringField('Model Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'), ('Coupe', 'Coupe')
    ], validators=[DataRequired()])
    transmission = SelectField('Transmission', choices=[
        ('Automatic', 'Automatic'), ('Manual', 'Manual')
    ], validators=[DataRequired()])
    fuel_type = SelectField('Fuel Type', choices=[
        ('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid')
    ], validators=[DataRequired()])
    seats = IntegerField('Seating Capacity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    price_per_day = DecimalField('Daily Price ($)', validators=[DataRequired(), NumberRange(min=0)])
    availability_status = SelectField('Status', choices=[
        ('available', 'Available'), ('booked', 'Booked'), ('maintenance', 'Maintenance')
    ], default='available')
    image = FileField('Vehicle Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    submit = SubmitField('Save Vehicle')