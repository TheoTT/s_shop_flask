import logging

from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from flask_cors import cross_origin
from marshmallow import fields
from sqlalchemy import or_

from hobbit_core.response import SuccessResult, ValidationErrorResult
from hobbit_core.utils import use_kwargs
from hobbit_core.db import transaction
from hobbit_core.pagination import PageParams, pagination

# from app.models import Menu, SubMenu  # NOQA
from app.models import Good, User, Order # NOQA
from app import schemas  # NOQA
from app.exts import db, photos


bp = Blueprint('orders', __name__)


@bp.route('/orders/', methods=['GET'])
@use_kwargs(PageParams)
@use_kwargs({'keyword': fields.Str(required=False)})
@jwt_required()
def list(page, page_size, order_by, keyword):
    qexp = Order.query
    if keyword:
        qexp = qexp.filter(Order.order_number.like(f'%{keyword}%'))
    paged_ret = pagination(Order, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_order_schemas.dump(paged_ret))


@bp.route('/orders/', methods=['POST'])
@use_kwargs(schemas.order_create_schema)
@jwt_required()
@transaction(db.session)
def create(
        order_number, trad_no, invoice_titile, invoice_company,
        invoice_content, consignee_address, order_price, pay_status,
        is_send, user_id, goods
    ):
    if Order.query.filter(or_(
            Order.order_number == order_number)).first():
        return ValidationErrorResult(message='Order已存在')
    order = Order(
        order_number=order_number, trad_no=trad_no,
        invoice_titile=invoice_titile, invoice_company=invoice_company,
        invoice_content=invoice_content, consignee_address=consignee_address,
        order_price=order_price, pay_status=pay_status,
        is_send=is_send)

    user = User.query.filter(User.id == user_id).one()
    if user:
        user.orders.append(order)
        order.user_id = user_id
    if goods:
        for good in goods:
            gd = Good.query.filter(Good.id == good['id']).one()
            if gd:
                order.goods.append(gd)
    db.session.add(order)
    db.session.flush()
    return jsonify(schemas.order_schema.dump(order)), 201


@bp.route('/orders/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve(pk):
    order = Order.query.filter(Order.id == pk).one()
    return jsonify(schemas.order_schema.dump(order)), 200


# @bp.route('/goods/<int:pk>/', methods=['PUT'])
# @use_kwargs(schemas.good_create_schema)
# @jwt_required()
# @transaction(db.session)
# def update(auth_name, path, parent_id, pk, level):

#     menu = Menu.query.filter(Menu.id == pk).one()
#     if not menu:
#         return ValidationErrorResult(
#             message='ID 为{pk} 菜单不存在')

#     menu.auth_name = auth_name
#     menu.path = path
#     menu.level = level
#     parent =Menu.query.filter(Menu.id == parent_id).one()
#     if parent and (menu not in parent.children):
#         parent.children.append(menu)
#     db.session.flush()

#     return jsonify(schemas.menu_schema.dump(menu)), 200


@bp.route('/orders/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete(pk):
    order = Order.query.filter(Order.id == pk).one()
    if not order:
        return ValidationErrorResult(
            message='ID 为{pk} Order不存在')
    db.session.delete(order)
    db.session.flush()
    return '', 204