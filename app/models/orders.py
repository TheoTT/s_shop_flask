import logging
import enum
from datetime import datetime
from hobbit_core.db import Column, BaseModel, reference_col, SurrogatePK
from sqlalchemy.orm import relationship, exc

from app.exts import db


goods_orders = db.Table(
    'association_order',
    Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    Column('good_id', db.Integer, db.ForeignKey('goods.id'))
)


class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(db.Integer, primary_key=True)
    order_number = Column(db.String(200), nullable=False, index=True)
    trad_no = Column(db.String(200), nullable=True)
    invoice_titile = Column(db.String(500), nullable=True)
    invoice_company = Column(db.String(500), nullable=True)
    invoice_content = Column(db.String(500), nullable=True)
    consignee_address = Column(db.String(500), nullable=True)
    order_price = Column(db.Float, nullable=False, default=1.0)
    pay_status = Column(
        db.Enum('未支付', '已支付', '已取消'),
        default='未支付', doc='订单状态:未支付, 已支付, 已取消')
    is_send = Column(db.Boolean(), default=False, doc='False代表非热销商品')

    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)

    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')

    goods = relationship('Good', secondary=goods_orders, back_populates="orders", lazy='dynamic')

    def __init__(
            self, order_number, trad_no, invoice_titile, invoice_company,
            invoice_content, consignee_address, order_price, pay_status,
            is_send, **kwargs):
        db.Model.__init__(
            self,
            order_number=order_number, trad_no=trad_no,
            invoice_titile=invoice_titile, invoice_company=invoice_company,
            invoice_content=invoice_content, consignee_address=consignee_address,
            order_price=order_price, pay_status=pay_status,
            is_send=is_send, **kwargs)
