from flask import _request_ctx_stack
from functools import wraps
from flask_jwt import _jwt
import jwt


def jwt_optional(realm=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = _jwt.request_callback()
            try:
                payload = _jwt.jwt_decode_callback(token)
            except jwt.exceptions.DecodeError:
                pass
            else:
                _request_ctx_stack.top.current_identity = _jwt.identity_callback(payload)
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def jwt_identity(payload):
    from app.models import User  # noqa
    user_id = payload['identity']
    return User.s_query().filter(User.id == user_id).first()


def authenticate(username, password):
    from app.models import User  # noqa
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

