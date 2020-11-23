from flask import render_template, Blueprint, request
from .forms import LoginForm, RegisterForm, ForgotForm

blueprint = Blueprint("pages", __name__)


################
#### routes ####
################


@blueprint.route("/")
def home():
    return render_template("pages/home_template.html")


@blueprint.route("/about")
def about():
    return render_template("pages/about_template.html")


@blueprint.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("forms/login.html", form=form)


@blueprint.route("/register")
def register():
    form = RegisterForm(request.form)
    return render_template("forms/register.html", form=form)


@blueprint.route("/forgot")
def forgot():
    form = ForgotForm(request.form)
    return render_template("forms/forgot.html", form=form)
