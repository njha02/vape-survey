from flask import Flask
from .views import blueprint as views
from flask_humanize import Humanize

import os
import yaml


def create_app(config={}):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(config)
    app.register_blueprint(views)
    Humanize(app)
    return app


with open("../secret.yaml") as f:
    secrets = yaml.load(f, Loader=yaml.SafeLoader)["env_variables"]

config = {
    "SECRET_KEY": secrets["SECRET_KEY"],
}


if os.environ.get("DEV_OVERRIDE_USER"):
    config["DEV_OVERRIDE_USER"] = os.environ["DEV_OVERRIDE_USER"]

app = create_app(config)
