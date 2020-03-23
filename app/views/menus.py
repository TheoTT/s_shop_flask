from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from flask_cors import cross_origin
from marshmallow import fields
from sqlalchemy import or_

from hobbit_core.response import SuccessResult, ValidationErrorResult
from hobbit_core.utils import use_kwargs
from hobbit_core.db import transaction
from hobbit_core.pagination import PageParams, pagination

from app.models import Menu  # NOQA
from app import schemas  # NOQA
from app.exts import db


bp = Blueprint('menu', __name__)

@bp.route('/menus/', methods=['GET'])
@use_kwargs(PageParams)
@jwt_required()
def list(page, page_size, order_by):
    print(dir(Menu))
    qexp = Menu.query
    paged_ret = pagination(Menu, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_menu_schemas.dump(paged_ret))


@bp.route('/menus/', methods=['POST'])
@use_kwargs(schemas.menu_create_schema)
@jwt_required()
@transaction(db.session)
def create(auth_name, path):
    if Menu.query.filter(or_(
            Menu.auth_name == auth_name)).first():
        return ValidationErrorResult(message='Menu已存在')
    menu = Menu(auth_name=auth_name, path=path)
    db.session.add(menu)
    db.session.flush()

    return jsonify(schemas.menu_schema.dump(menu)), 201


@bp.route('/menus/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve(pk):
    user = Menu.query.filter(Menu.id == pk).one()
    return jsonify(schemas.menu_schema.dump(user)), 200


@bp.route('/menus/<int:pk>/', methods=['PUT'])
@use_kwargs(schemas.menu_create_schema)
@jwt_required()
@transaction(db.session)
def update(auth_name, path, child_id, pk):

    menu = Menu.query.filter(Menu.id == pk).one()
    if not menu:
        return ValidationErrorResult(
            message='ID 为{pk} 菜单不存在')

    menu.auth_name = auth_name
    menu.path = path
    child = Menu.query.filter(Menu.id == child_id).one()
    if child:
        menu.sub_menu.append(child)
    db.session.flush()

    return jsonify(schemas.menu_schema.dump(menu)), 200


@bp.route('/menus/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete(pk):
    menu = Menu.query.filter(Menu.id == pk).one()
    if not Menu:
        return ValidationErrorResult(
            message='ID 为{pk} Menu不存在')
    db.session.delete(menu)
    db.session.flush()
    return '', 204