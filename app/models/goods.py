import logging
from datetime import datetime
from hobbit_core.db import Column, BaseModel, reference_col, SurrogatePK
from sqlalchemy.orm import relationship, exc

from app.exts import bcrypt, db
# from app.models import Role # (ORM之间的model不需要互相导入，可以直接使用)


class Good(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key = True)
    good_name = Column(db.String(32), nullable=False, index=True)
    good_price = Column(db.Float, nullable=False, default=1.0)
    good_number = Column(db.Integer, nullable=False, default=1)
    good_state = Column(db.Boolean(), default=True, doc='1代表激活')
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    # parent_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    # children = db.relationship('Good', back_populates='parent')
    # parent = db.relationship('Good', back_populates='children', remote_side=[id])

    # role_id = Column(db.Integer, db.ForeignKey('roles.id'))
    # role = relationship('Role', backref=db.backref('menus', order_by=id))
    # roles = relationship('Role', secondary=association_table, back_populates="menus")
    # 将back_populates修改为db.backref() 指定 lazy = 'dynamic' 参数，关系两侧返回的查询都可接受额外的过滤器
    # roles = relationship('Role', secondary=association_table, backref=db.backref("menus", lazy='dynamic'))

    def __init__(self, good_name, **kwargs):
        db.Model.__init__(self, good_name=good_name, **kwargs)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    category_name = Column(db.String(32), nullable=False, index=True)
    category_desc = Column(db.String(200), nullable=True)
    category_level = Column(db.Integer, nullable=True)
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    children = db.relationship('Category', back_populates='parent')
    parent = db.relationship('Category', back_populates='children', remote_side=[id])
    # parent = db.relationship('Category', backref=db.backref("children", lazy='dynamic'), remote_side=[id])

    # role_id = Column(db.Integer, db.ForeignKey('roles.id'))
    # role = relationship('Role', backref=db.backref('menus', order_by=id))
    # roles = relationship('Role', secondary=association_table, back_populates="menus")
    # 将back_populates修改为db.backref() 指定 lazy = 'dynamic' 参数，关系两侧返回的查询都可接受额外的过滤器
    # roles = relationship('Role', secondary=association_table, backref=db.backref("menus", lazy='dynamic'))

    def __init__(self, category_name, category_level, category_desc, **kwargs):
        db.Model.__init__(
            self, category_name=category_name, category_level=category_level,
             category_desc=category_desc, **kwargs)

    @property
    def children_f(self, type=2):
        children = []
        if type == 1:
            return children

        categories_1 = self.children
        logging.error(categories_1)
        for category_1 in categories_1:
            if type == 2:
                item_1 = {}
                children_1 = []
                for category_2 in category_1.children:
                    children_1.append(category_2)
                item_1 = {
                    'children': [],
                    # 'children_f': [],
                    'category_name': category_1.category_name,
                    'category_desc': category_1.category_desc,
                    'category_level': category_1.category_level,
                    'id': category_1.id,
                    'parent_id': category_1.parent_id,
                    'parent': category_1.parent,
                    'updated_at': category_1.updated_at,
                    'created_at': category_1.created_at
                }
                children.append(item_1)
            else:
                children.append(category_1)
        return children
