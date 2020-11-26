from flask import render_template, Blueprint, request, redirect, flash, current_app
from .forms import SurveyForm
import hashlib

from .sheets import write_to_sheet

blueprint = Blueprint("pages", __name__)


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = SurveyForm(request.form)

    if form.validate_on_submit():
        submit_to_sheet(form.data)
        return redirect("/thankyou")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    u"Error in the %s field - %s"
                    % (getattr(form, field).label.text, error),
                    "error",
                )
    return render_template("forms/survey.html", form=form)


@blueprint.route("/thankyou", methods=["GET"])
def thankyou():
    return render_template("pages/thankyou_template.html")


def submit_to_sheet(data):
    del data["csrf_token"]

    def encrypt_string(s):
        return hashlib.sha512(str.encode(s)).hexdigest()

    data["name"] = encrypt_string(data["name"].strip().lower())
    data["friend1"] = encrypt_string(data["friend1"].strip().lower())
    data["friend2"] = encrypt_string(data["friend2"].strip().lower())
    data["friend3"] = encrypt_string(data["friend3"].strip().lower())
    if "email" in data:
        email = data["email"]
        write_to_sheet("emails", [email])
        del data["email"]
    write_to_sheet(
        data["school"], list(data.values())
    )  # TODO: should be explicit about what fields we expect to recieve
