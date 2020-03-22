from hobbit_core.db import Column, BaseModel
from flask_jwt import _default_jwt_encode_handler

from app.exts import bcrypt, db


class User(BaseModel):
    exclude_columns = ['created_at', 'updated_at']
    username = Column(db.String(32), nullable=False, index=True)
    password = Column(db.String(256), nullable=False)
    del_flag = Column(db.Integer(), default=0, doc='0代表未删除')

    def __init__(self, username, password=None, **kwargs):
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    @classmethod
    def s_query(cls):
        """查询激活状态的user，未被删除
        """
        return cls.query.filter_by(del_flag=0)

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def token(self):
        return _default_jwt_encode_handler(self).decode('utf-8')




