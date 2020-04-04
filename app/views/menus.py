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
from app.models import Menu  # NOQA
from app import schemas  # NOQA
from app.exts import db


bp = Blueprint('menu', __name__)

@bp.route('/menus/', methods=['GET'])
@use_kwargs(PageParams)
@jwt_required()
def list(page, page_size, order_by):
    qexp = Menu.query
    paged_ret = pagination(Menu, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_menu_schemas.dump(paged_ret))

@bp.route('/menus_aside/', methods=['GET'])
@use_kwargs(PageParams)
@jwt_required()
def list_aside(page, page_size, order_by):
    qexp = Menu.query.filter_by(level=0)
    paged_ret = pagination(Menu, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_menu_schemas.dump(paged_ret))

@bp.route('/menus/', methods=['POST'])
@use_kwargs(schemas.menu_create_schema)
@jwt_required()
@transaction(db.session)
def create(auth_name, path, level):
    if Menu.query.filter(or_(
            Menu.auth_name == auth_name)).first():
        return ValidationErrorResult(message='Menu已存在')
    menu = Menu(level=level, auth_name=auth_name, path=path)
    db.session.add(menu)
    db.session.flush()

    return jsonify(schemas.menu_schema.dump(menu)), 201


@bp.route('/menus/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve(pk):
    menu = Menu.query.filter(Menu.id == pk).one()
    return jsonify(schemas.menu_schema.dump(menu)), 200


@bp.route('/menus/<int:pk>/', methods=['PUT'])
@use_kwargs(schemas.menu_create_schema)
@jwt_required()
@transaction(db.session)
def update(auth_name, path, parent_id, pk, level):

    menu = Menu.query.filter(Menu.id == pk).one()
    if not menu:
        return ValidationErrorResult(
            message='ID 为{pk} 菜单不存在')

    menu.auth_name = auth_name
    menu.path = path
    menu.level = level
    parent =Menu.query.filter(Menu.id == parent_id).one()
    if parent and (menu not in parent.children):
        parent.children.append(menu)
    db.session.flush()

    return jsonify(schemas.menu_schema.dump(menu)), 200


@bp.route('/menus/<int:pk>/children/', methods=['PUT'])
@use_kwargs({'children': fields.List(fields.Integer(), required=True)})
@jwt_required()
@transaction(db.session)
def update_children(children, pk):

    menu = Menu.query.filter(Menu.id == pk).one()
    if not menu:
        return ValidationErrorResult(
            message='ID 为{pk} 菜单不存在')
    if children:
        menus = Menu.query.filter(Menu.id.in_(children)).all()
        menu.children = menus
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

# @bp.route('/sub_menus/', methods=['GET'])
# @use_kwargs(PageParams)
# @jwt_required()
# def sub_list(page, page_size, order_by):
#     qexp = SubMenu.query
#     paged_ret = pagination(SubMenu, page, page_size, order_by, query_exp=qexp)
#     return jsonify(schemas.paged_sub_menu_schemas.dump(paged_ret))


# @bp.route('/sub_menus/', methods=['POST'])
# @use_kwargs(schemas.sub_menu_create_schema)
# @jwt_required()
# @transaction(db.session)
# def sub_create(auth_name, path):
#     if SubMenu.query.filter(or_(
#             SubMenu.auth_name == auth_name)).first():
#         return ValidationErrorResult(message='SubMenu已存在')
#     sub_menu = SubMenu(auth_name=auth_name, path=path)
#     db.session.add(sub_menu)
#     db.session.flush()

#     return jsonify(schemas.sub_menu_schema.dump(sub_menu)), 201


# @bp.route('/sub_menus/<int:pk>/', methods=['GET'])
# @jwt_required()
# def sub_retrieve(pk):
#     sub_menu = SubMenu.query.filter(SubMenu.id == pk).one()
#     return jsonify(schemas.sub_menu_schema.dump(sub_menu)), 200


# @bp.route('/sub_menus/<int:pk>/', methods=['PUT'])
# @use_kwargs(schemas.sub_menu_create_schema)
# @jwt_required()
# @transaction(db.session)
# def sub_update(auth_name, path, pk):

#     sub_menu = SubMenu.query.filter(SubMenu.id == pk).one()
#     if not sub_menu:
#         return ValidationErrorResult(
#             message='ID 为{pk} 菜单不存在')

#     sub_menu.auth_name = auth_name
#     sub_menu.path = path
#     db.session.flush()

#     return jsonify(schemas.sub_menu_schema.dump(sub_menu)), 200


# @bp.route('/sub_menus/<int:pk>/', methods=['DELETE'])
# @jwt_required()
# @transaction(db.session)
# def sub_delete(pk):
#     sub_menu = SubMenu.query.filter(SubMenu.id == pk).one()
#     if not sub_menu:
#         return ValidationErrorResult(
#             message='ID 为{pk} SubMenu不存在')
#     db.session.delete(sub_menu)
#     db.session.flush()
#     return '', 204