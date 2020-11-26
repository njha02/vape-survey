import os
import yaml

from webapp.app import create_app


with open("./secret.yaml") as f:
    secrets = yaml.load(f, Loader=yaml.SafeLoader)["env_variables"]

config = {"SECRET_KEY": secrets["SECRET_KEY"]}


if os.environ.get("DEV_OVERRIDE_USER"):
    config["DEV_OVERRIDE_USER"] = os.environ["DEV_OVERRIDE_USER"]

app = create_app(config)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
