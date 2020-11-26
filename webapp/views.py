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
                    "Error in the %s field - %s"
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

    for x in [
        "School",
        "Name",
        "Email",
        "Age",
        "Grade",
        "Gender",
        "Closest 1",
        "Closest 2",
        "Closest 3",
        "Influence",
        "Vape",
    ]:
        assert x in data

    data["Name"] = encrypt_string(data["Name"].strip().lower())
    data["Closest 1"] = encrypt_string(data["Closest 1"].strip().lower())
    data["Closest 2"] = encrypt_string(data["Closest 2"].strip().lower())
    data["Closest 3"] = encrypt_string(data["Closest 3"].strip().lower())
    if "Email" in data:
        email = data["Email"]
        write_to_sheet(f"{data['School']} Emails", [email])
        del data["Email"]
    write_to_sheet(
        data["School"],
        [
            data["School"],
            data["Name"],
            data["Age"],
            data["Grade"],
            data["Gender"],
            data["Closest 1"],
            data["Closest 2"],
            data["Closest 3"],
            data["Influence"],
            data["Vape"],
        ],
    )


@blueprint.route("/about", methods=["GET"])
def about():
    return render_template("pages/about_template.html")  #
