from flask_wtf import Form
from wtforms import TextField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Length
from .models import (
    Question,
    SelectQuestion,
    EmailQuestion,
    IntegerQuestion,
    load_from_yaml,
)


def question_to_field(q: Question):
    validators = []
    if q.required:
        validators.append(DataRequired())
    if isinstance(q, SelectQuestion):
        return SelectField(
            description=q.description,
            choices=[(x, x) for x in q.choices],
            validators=validators + [Length(min=6, max=25)],
            render_kw={"class": "form-control"},
        )
    elif isinstance(q, EmailQuestion):
        return EmailField(
            description=q.description,
            validators=validators + [Length(min=6, max=25)],
            render_kw={"class": "form-control"},
        )
    elif isinstance(q, IntegerQuestion):
        return IntegerField(
            description=q.description,
            validators=validators,
            render_kw={"class": "form-control"},
        )

    else:  # Basic text question
        return TextField(
            description=q.description,
            validators=validators + [Length(min=6, max=25)],
            render_kw={"class": "form-control"},
        )


questions = load_from_yaml()


class SurveyForm(Form):
    questions = questions


for q in questions:
    setattr(SurveyForm, q.q_key, question_to_field(q))
