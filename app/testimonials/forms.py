from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class TestimonialForm(FlaskForm):
    message = TextAreaField("Your testimonial",
                            validators=[DataRequired(), Length(min=10, max=1000)])
    rating = IntegerField("Rating (1-5)",
                          validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField("Submit testimonial")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    message = TextAreaField("Message",
                            validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField("Send message")


class SubscribeForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    submit = SubmitField("Subscribe")