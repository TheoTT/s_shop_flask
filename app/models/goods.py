import logging
import enum
from datetime import datetime
from hobbit_core.db import Column, BaseModel, reference_col, SurrogatePK
from sqlalchemy.orm import relationship, exc

from app.exts import bcrypt, db
from app.models.orders import goods_orders
# from app.models import Role # (ORM之间的model不需要互相导入，可以直接使用)


class Good(db.Model):
    __tablename__ = 'goods'
    id = Column(db.Integer, primary_key=True)
    good_name = Column(db.String(32), nullable=False, index=True)
    good_desc = Column(db.String(200), nullable=True)
    good_price = Column(db.Float, nullable=False, default=1.0)
    good_weight = Column(db.Float, nullable=False, default=1.0)
    good_number = Column(db.Integer, nullable=False, default=1)
    hot_number = Column(db.Integer, nullable=False, default=1)
    good_state = Column(
        db.Enum('ReviewFaild', 'UnderReview', 'Reviewed'),
        default='UnderReview', doc='商品状态:未通过, 审核中, 已审核')
    is_promote = Column(db.Boolean(), default=False, doc='False代表非热销商品')

    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)

    category_id = Column(db.Integer, db.ForeignKey('categories.id'))
    category = relationship('Category', back_populates='goods')
    photos = relationship('Photo', back_populates='good', lazy='dynamic')
    orders = relationship('Order', secondary=goods_orders, back_populates="goods", lazy='dynamic')


    def __init__(
            self, good_name, good_price, good_weight, good_number,
            good_desc, hot_number,
            good_state, is_promote, **kwargs):
        db.Model.__init__(
            self, good_name=good_name, good_state=good_state,
            good_price=good_price, good_number=good_number,
            good_weight=good_weight, good_desc=good_desc,
            hot_number=hot_number, is_promote=is_promote, **kwargs)


class Attribute(db.Model):
    __tablename__ = 'attributes'

    class Sel(enum.Enum):
        only = 0
        many = 1

    class Write(enum.Enum):
        manual = 0
        list = 1

    id = db.Column(db.Integer, primary_key=True)
    attribute_name = Column(db.String(32), nullable=False, index=True)
    # attribute_sel = Column(db.Enum(Sel), default=Sel.only, nullable=False)
    attribute_sel = Column(db.Enum('only', 'many'), default='only', nullable=False)
    attribute_write = Column(db.Enum('manual', 'list'), default='list', nullable=False)
    # attribute_write = Column(db.Enum(Write), default=Write.list, nullable=False)
    attribute_values = Column(db.String(200), nullable=True, index=True)
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    category_id = Column(db.Integer, db.ForeignKey('categories.id'))
    category = relationship('Category', back_populates='attributes')

    def __init__(
        self, attribute_name, attribute_sel, attribute_write,
        attribute_values='', **kwargs):
        db.Model.__init__(
            self, attribute_name=attribute_name, attribute_sel=attribute_sel,
            attribute_write=attribute_write, attribute_values=attribute_values,
            **kwargs)


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_name = Column(db.String(500), nullable=False, index=True)
    # photo_url = Column(db.Url(), nullable=False, index=True)
    photo_url = Column(db.String(500), nullable=False, index=True)
    good_id = Column(db.Integer, db.ForeignKey('goods.id'))
    good = relationship('Good', back_populates='photos')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = Column(db.String(32), nullable=False, index=True)
    category_desc = Column(db.String(200), nullable=True)
    category_level = Column(db.Integer, nullable=True)
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    children = db.relationship('Category', back_populates='parent')
    attributes = db.relationship('Attribute', back_populates='category', lazy='dynamic')
    goods = db.relationship('Good', back_populates='category', lazy='dynamic')
    parent = db.relationship('Category', back_populates='children', remote_side=[id])
    # parent = db.relationship('Category', backref=db.backref("children", lazy='dynamic'), remote_side=[id])

    # role_id = Column(db.Integer, db.ForeignKey('roles.id'))
    # role = relationship('Role', backref=db.backref('menus', order_by=id))
    # roles = relationship('Role', secondary=association_table, back_populates="menus")
    # 将back_populates修改为db.backref() 指定 lazy = 'dynamic' 参数，关系两侧返回的查询都可接受额外的过滤器
    # roles = relationship('Role', secondary=association_table, backref=db.backref("menus", lazy='dynamic'))

    def __init__(self, category_name, category_level, category_desc, **kwargs):
        db.Model.__init__(
            self, category_name=category_name, category_level=category_level, **kwargs)

    @property
    def children_f(self, type=2):
        children = []
        if type == 1:
            return children

        categories_1 = self.children
        # logging.error(categories_1)
        for category_1 in categories_1:
            if type == 2:
                item_1 = {}
                children_1 = []
                for category_2 in category_1.children:
                    children_1.append(category_2)
                item_1 = {
                    'children_f': [],
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
                if item_1['children_f'] == []:
                    del(item_1['children_f'])
                children.append(item_1)
            else:
                children.append(category_1)
        return children

    @property
    def children_p(self):
        children = []
        categories_1 = self.children
        logging.error(f'all: {categories_1}')
        for category_1 in categories_1:
            children_1 = []
            for category_2 in category_1.children:
                item_2 = {
                    'category_name': category_2.category_name,
                    'category_desc': category_2.category_desc,
                    'category_level': category_2.category_level,
                    'id': category_2.id,
                    'parent_id': category_2.parent_id,
                    'parent': category_2.parent,
                    'updated_at': category_2.updated_at,
                    'created_at': category_2.created_at
                }
                children_1.append(item_2)          
            item_1 = {
                'children_p': children_1,
                'category_name': category_1.category_name,
                'category_desc': category_1.category_desc,
                'category_level': category_1.category_level,
                'id': category_1.id,
                'parent_id': category_1.parent_id,
                'parent': category_1.parent,
                'updated_at': category_1.updated_at,
                'created_at': category_1.created_at
            }
            logging.error(f'{category_1.category_name}: {item_1}')
            if item_1['children_p'] == []:
                del(item_1['children_p'])
            logging.error(f'{category_1.category_name}: {item_1}')

            children.append(item_1)
        logging.error(f'aaaaa: {children}')
        return children
