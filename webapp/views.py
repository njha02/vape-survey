from flask import render_template, Blueprint, request, redirect, flash, current_app
from .forms import SurveyForm
from google.cloud import storage
import json
from cryptography.fernet import Fernet


blueprint = Blueprint("pages", __name__)



@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = SurveyForm(request.form)
    if form.validate_on_submit():
        write_to_storage(form.data)
        return redirect('/thankyou')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ), 'error')
    return render_template("forms/survey.html", form=form)


@blueprint.route("/thankyou", methods=["GET"])
def thankyou():
    return render_template("pages/thankyou_template.html")


def write_to_storage(data):
    client = storage.Client.from_service_account_json(
        '../secret.json'
    )
    bucket = client.bucket("vape-survey-results")

    def encrypt_data(data):
        def encrypt_string(s):
            return Fernet(current_app.config["ENCRYPTION_KEY"]).encrypt(str.encode(s)).decode()
        data["name"] = encrypt_string(data["name"].strip().lower())
        data["friend1"] = encrypt_string(data["friend1"].strip().lower())
        data["friend2"] = encrypt_string(data["friend2"].strip().lower())
        data["friend3"] = encrypt_string(data["friend3"].strip().lower())
        return data

    data = encrypt_data(data)
    print("Encrypted data", data)

    filename = f'{data["name"]}.json'
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(data))
    print(
        "Data {} uploaded to {}.".format(
            data, filename
        )
    )

    destination = bucket.blob("data.json")
    destination.content_type = "text/plain"
    destination.compose([blob, destination])
    print(
        "Composed new object {} in the bucket {}".format(
            "data.json", bucket.name
        )
    )
