from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from flask_cors import cross_origin
from marshmallow import fields
from sqlalchemy import or_

from hobbit_core.response import SuccessResult, ValidationErrorResult
from hobbit_core.utils import use_kwargs
from hobbit_core.db import transaction
from hobbit_core.pagination import PageParams, pagination

from app.models import User  # NOQA
from app import schemas  # NOQA
from app.exts import db

bp = Blueprint('user', __name__)

#@cross_origin(allow_headers=['Content-Type'])
@bp.route('/login/', methods=['POST'])
@use_kwargs(schemas.user_schema)
def login(username, password):
    user = User.s_query().filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return ValidationErrorResult(message='错误的用户名或者密码')
    return jsonify(schemas.token_schema.dump(user)), 201


@bp.route('/logout/', methods=['POST'])
@jwt_required()
def logout():
    return SuccessResult(status=201)


@bp.route('/users/', methods=['GET'])
@use_kwargs(PageParams)
@jwt_required()
def list(page, page_size, order_by):
    qexp = User.s_query()
    paged_ret = pagination(User, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_user_schemas.dump(paged_ret))


@bp.route('/users/', methods=['POST'])
@use_kwargs(schemas.user_create_schema)
# @jwt_required()
@transaction(db.session)
def create(username, password):
    if User.s_query().filter(or_(
            User.username == username)).first():
        return ValidationErrorResult(message='用户名或者邮箱已存在')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.flush()

    return jsonify(schemas.user_schema.dump(user)), 201


@bp.route('/users/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve(pk):
    user = User.s_query().filter(User.id == pk).one()
    return jsonify(schemas.user_schema.dump(user)), 200


@bp.route('/users/<int:pk>/', methods=['PUT'])
@use_kwargs(schemas.user_create_schema)
@jwt_required()
@transaction(db.session)
def update(username, password, email, pk):

    user = User.s_query().filter(User.id == pk).one()
    if not user:
        return ValidationErrorResult(
            message='ID 为{pk} 用户不存在')

    user.set_password(password)
    user.username = username
    user.email = email
    db.session.flush()

    return jsonify(schemas.user_schema.dump(user)), 200


@bp.route('/users/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete(pk):
    user = User.s_query().filter(User.id == pk).one()
    if not user:
        return ValidationErrorResult(
            message='ID 为{pk} 用户不存在')
    user.del_flag = user.id
    return '', 204
