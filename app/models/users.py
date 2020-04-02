import logging
import copy
from datetime import datetime
from hobbit_core.db import Column, BaseModel
from flask_jwt import _default_jwt_encode_handler
from sqlalchemy.orm import relationship, exc

from app.exts import bcrypt, db
from app.models.menus import association_table


class User(db.Model):
    # 包含在exclude_columns 的列不会新建
    # exclude_columns = ['created_at', 'updated_at']
    __tablename__ = 'users'
    id = Column(db.Integer, primary_key = True)
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    username = Column(db.String(32), nullable=False, index=True)
    password = Column(db.String(256), nullable=False)
    email = Column(db.String(32), nullable=False, index=True)
    # status = Column(db.Integer(), default=1, doc='1代表激活')
    status = Column(db.Boolean(), default=True, doc='1代表激活')
    del_flag = Column(db.Integer(), default=0, doc='0代表未删除')
    role_id = Column(db.Integer, db.ForeignKey('roles.id'))
    role = relationship('Role', backref=db.backref('users', order_by=username))

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
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


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(db.Integer, primary_key = True)
    # exclude_columns = ['created_at', 'updated_at']
    role_name = Column(db.String(32), nullable=False, index=True)
    role_desc = Column(db.String(256), nullable=True, index=False)
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    # menus = relationship('Menu', secondary=association_table, back_populates="roles")

    def __init__(self, role_name, role_desc, **kwargs):
        db.Model.__init__(self, role_name=role_name, role_desc=role_desc, **kwargs)

    @property
    def role_menus(self):
        # TODO 优化角色对应权限的筛选逻辑
        menus = []
        menus_1 = self.menus.filter_by(level=0).all()
        # logging.error(menus_1)
        for menu_1 in menus_1:
            # menu_1 = copy.deepcopy(menu_1_o)
            item_1 = {}
            children_1 = []
            # logging.error((menu_1.children, self.menus.all()))
            for menu_2 in menu_1.children:
                # menu_2 = copy.deepcopy(menu_2_o)
                item_2 = {}
                children_2 = []
                if menu_2 in self.menus.all():
                    # children_1.append(menu_2) 
                    for menu_3 in menu_2.children:
                        if menu_3 in self.menus.all():
                            children_2.append(menu_3)
                    item_2 = {
                        'children': children_2,
                        'auth_name': menu_2.auth_name,
                        'created_at': menu_2.created_at,
                        'id': menu_2.id,
                        'level': menu_2.level,
                        'path': menu_2.path,
                        'updated_at': menu_2.updated_at
                    }
                    children_1.append(item_2)
            item_1 = {
                'children': children_1,
                'auth_name': menu_1.auth_name,
                'created_at': menu_1.created_at,
                'id': menu_1.id,
                'level': menu_1.level,
                'path': menu_1.path,
                'updated_at': menu_1.updated_at
            }
            menus.append(item_1)
        return menus
        