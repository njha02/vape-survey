from flask_wtf import Form
from wtforms import TextField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Length


class SurveyForm(Form):
    school = SelectField(
        label="School",
        choices=[
            ("School1", "School 1"),
            ("School2", "School 2"),
            ("School3", "School 3"),
        ],
    )
    name = TextField(label="Name", validators=[DataRequired(), Length(min=6, max=25)])
    email = EmailField(
        label="Email", validators=[DataRequired(), Length(min=6, max=40)]
    )
    age = IntegerField(label="Age", validators=[DataRequired()])
    grade = SelectField(
        label="Grade Level",
        choices=[("9", "9th"), ("10", "10th"), ("11", "11th"), ("12", "12th")],
    )
    gender = SelectField(
        label="Gender",
        choices=[
            ("Female", "Female"),
            ("Male", "Male"),
            ("Other", "Other"),
            ("Prefer not to say", "Prefer not to say"),
        ],
    )
    friend1 = TextField(
        label="Closest Friend", validators=[DataRequired(), Length(min=6, max=25)]
    )
    friend2 = TextField(
        label="2nd Closest Friend", validators=[DataRequired(), Length(min=6, max=25)]
    )
    friend3 = TextField(
        label="3rd Closest Friend", validators=[DataRequired(), Length(min=6, max=25)]
    )
    influence = SelectField(
        label="I think my friends strongly influence my actions",
        choices=[("True", "True"), ("False", "False")],
    )
    vape = SelectField(
        label="I vape at least once every two weeks.",
        choices=[("True", "True"), ("False", "False")],
    )
