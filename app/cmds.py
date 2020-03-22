from flask.cli import AppGroup, with_appcontext
from flask import current_app

from app.models import User  # NOQA


#db = current_app.db

cli = AppGroup('shop', help='shop.')

@cli.command()
@with_appcontext
@transaction(db.session)
def init_user():
    root_user = User.s_query().filter_by(username='root').one_or_none()
    if not root_user:
        root_user = User(username='admin', password='123456')
        db.session.add(root_user)
        db.session.flush()


cmd_list = [init_user]


