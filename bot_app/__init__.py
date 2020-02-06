import os
from flask import Flask
from bot_app.controller import anonymous_controller as anonymous
from bot_app.controller import interacitve_controller as interactive
from . import config

config_type = {
  "development":  "bot_app.config.dev",
  "production": "bot_app.config.prod"
}

def create_app():
  app = Flask(__name__)
  app.config.from_object(config_type[os.getenv('FLASK_APP_ENV', 'production')])

  app.register_blueprint(anonymous.bp)
  app.register_blueprint(interactive.bp)

  return app

app = create_app()