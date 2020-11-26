from flask_wtf import Form
from wtforms import TextField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Length


class SurveyForm(Form):
    school = SelectField(
        description="Select your school:",
        label="School",
        choices=[
            ("School1", "School 1"),
            ("School2", "School 2"),
            ("School3", "School 3"),
        ],
    )
    name = TextField(
        description="Please type your FIRST and LAST name:",
        label="Name",
        validators=[DataRequired(), Length(min=6, max=25)],
    )
    email = EmailField(
        description="If you wish to be entered into a drawing for an Amazon eGift card, submit your email address. Your data will be anonymized and will not be linked to your survey results.",
        label="Email",
        validators=[Length(min=6, max=40)],
    )
    age = IntegerField(
        description="How old are you?", label="Age", validators=[DataRequired()]
    )
    grade = SelectField(
        description="Please select your grade level:",
        label="Grade Level",
        choices=[("9", "9th"), ("10", "10th"), ("11", "11th"), ("12", "12th")],
    )
    gender = SelectField(
        description="Please select your gender:",
        label="Gender",
        choices=[
            ("Female", "Female"),
            ("Male", "Male"),
            ("Other", "Other"),
            ("Prefer not to say", "Prefer not to say"),
        ],
    )
    friend1 = TextField(
        description="Write the FIRST and LAST name of your three closest friends:",
        label="Closest Friend",
        validators=[DataRequired(), Length(min=6, max=25)],
    )
    friend2 = TextField(
        description="Write the FIRST and LAST name of your three closest friends:",
        label="2nd Closest Friend",
        validators=[DataRequired(), Length(min=6, max=25)],
    )
    friend3 = TextField(
        description="Write the FIRST and LAST name of your three closest friends:",
        label="3rd Closest Friend",
        validators=[DataRequired(), Length(min=6, max=25)],
    )
    influence = SelectField(
        description="True/False: I think my friends strongly inuence my actions.",
        label="I think my friends strongly influence my actions",
        choices=[("True", "True"), ("False", "False")],
    )
    vape = SelectField(
        description="True/False: I vape (at least once every two weeks).",
        label="I vape at least once every two weeks.",
        choices=[("True", "True"), ("False", "False")],
    )
