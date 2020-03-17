from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from hobbit_core import HobbitManager

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
hobbit = HobbitManager()
