import os
import yaml

try:
    from webapp.app import create_app
except (ModuleNotFoundError, ImportError) as e:
    from .webapp.app import create_app


with open("./secret.yaml") as f:
    secrets = yaml.load(f, Loader=yaml.SafeLoader)["env_variables"]

config = {"SECRET_KEY": secrets["SECRET_KEY"]}


if os.environ.get("DEV_OVERRIDE_USER"):
    config["DEV_OVERRIDE_USER"] = os.environ["DEV_OVERRIDE_USER"]

app = create_app(config)
