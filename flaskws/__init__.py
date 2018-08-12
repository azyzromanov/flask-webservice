from flask import Flask
from .app import app
from . import models


# Connect sqlalchemy to app
models.db.init_app(app)
models.db.create_all()