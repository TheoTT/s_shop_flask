from flask_sqlalchemy import SQLAlchemy, Model
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from flask_cors import CORS

from hobbit_core import HobbitManager

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
hobbit = HobbitManager()
bcrypt = Bcrypt()
cors = CORS(resources=r"/*", origins=r"*", )

from app.core.jwt import authenticate, jwt_identity  # NOQA
jwt = JWT(authentication_handler=authenticate, identity_handler=jwt_identity)
