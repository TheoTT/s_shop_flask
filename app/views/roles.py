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

# from app.models import role, Subrole  # NOQA
from app.models import Role, Menu  # NOQA
from app import schemas  # NOQA
from app.exts import db


bp = Blueprint('role', __name__)

@bp.route('/roles/', methods=['GET'])
@use_kwargs(PageParams)
@jwt_required()
def list(page, page_size, order_by):
    qexp = Role.query
    paged_ret = pagination(Role, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_role_schemas.dump(paged_ret))


@bp.route('/roles/', methods=['POST'])
@use_kwargs(schemas.role_schema)
@jwt_required()
@transaction(db.session)
def create(role_name, role_desc):
    if Role.query.filter(or_(
            Role.role_name == role_name)).first():
        return ValidationErrorResult(message='role已存在')
    role = Role(role_name=role_name, role_desc=role_desc)
    db.session.add(role)
    db.session.flush()

    return jsonify(schemas.role_schema.dump(role)), 201


@bp.route('/roles/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve(pk):
    role = Role.query.filter(Role.id == pk).one()
    return jsonify(schemas.role_schema.dump(role)), 200


@bp.route('/roles/<int:pk>/menus/', methods=['DELETE'])
@jwt_required()
@use_kwargs({'menu_id': fields.Integer(required=True)})
@transaction(db.session) # 会进行db.commint操作
def remove_menu(pk, menu_id):
    role = Role.query.filter(Role.id == pk).one()
    # logging.error(role.menus.all())
    # logging.error(schemas.role_schema.dump(role))
    menu = Menu.query.filter(Menu.id == menu_id).one()
    if not role or not menu:
        return ValidationErrorResult(
            message=f'ID 为{pk} role不存在 或者ID为{menu_id} Menu不存在')
    if menu not in role.menus.all():
        return ValidationErrorResult(
            message=f'当前role中不存在ID为{menu_id} 的权限')
    role.menus.remove(menu)
    # logging.error(role.menus.all())
    db.session.flush()
    return jsonify(schemas.role_schema.dump(role)), 204


@bp.route('/roles/<int:pk>/', methods=['PUT'])
@use_kwargs(schemas.role_mod_schema)
@jwt_required()
@transaction(db.session)
def update(role_name, role_desc, menu_ids, pk):

    role = Role.query.filter(Role.id == pk).one()
    if not role:
        return ValidationErrorResult(
            message='ID 为{pk} Role不存在')

    role.role_name = role_name
    role.role_desc = role_desc
    if menu_ids:
        menus = Menu.query.filter(Menu.id.in_(menu_ids)).all()
        role.menus = menus

    db.session.flush()
    return jsonify(schemas.role_schema.dump(role)), 200


@bp.route('/roles/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete(pk):
    role = role.query.filter(role.id == pk).one()
    if not role:
        return ValidationErrorResult(
            message='ID 为{pk} role不存在')
    db.session.delete(role)
    db.session.flush()
    return '', 204