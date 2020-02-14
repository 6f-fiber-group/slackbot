import os
from flask import Flask
from backend.controller import anonymous_controller as anonymous
from backend.controller import interacitve_controller as interactive
from backend import config

config_type = {
  "development": "backend.config.dev",
  "production": "backend.config.prod"
}

def create_app():
  app = Flask(
    __name__,
    static_folder= "../frontend/dist/static",
    template_folder = "../frontend/dist/"
  )
  app.config.from_object(config_type[os.getenv('FLASK_APP_ENV', 'production')])

  app.register_blueprint(anonymous.bp)
  app.register_blueprint(interactive.bp)

  return app

app = create_app()