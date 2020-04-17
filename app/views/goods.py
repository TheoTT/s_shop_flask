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
from app.models import Good, Category, Attribute, Photo # NOQA
from app import schemas  # NOQA
from app.exts import db, photos


bp = Blueprint('goods', __name__)


@bp.route('/goods/', methods=['GET'])
@use_kwargs(PageParams)
@use_kwargs({'keyword': fields.Str(required=False)})
@jwt_required()
def list(page, page_size, order_by, keyword):
    qexp = Good.query
    if keyword:
        qexp = qexp.filter(Good.good_name.like(f'%{keyword}%'))
    paged_ret = pagination(Good, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_good_schemas.dump(paged_ret))

# @bp.route('/menus_aside/', methods=['GET'])
# @use_kwargs(PageParams)
# @jwt_required()
# def list_aside(page, page_size, order_by):
#     qexp = Menu.query.filter_by(level=0)
#     paged_ret = pagination(Menu, page, page_size, order_by, query_exp=qexp)
#     return jsonify(schemas.paged_menu_schemas.dump(paged_ret))

@bp.route('/goods/', methods=['POST'])
@use_kwargs(schemas.good_create_schema)
@jwt_required()
@transaction(db.session)
def create(
        good_name, good_price, good_weight, good_number,
        category_id, photos, good_desc,attributes, hot_number,
        good_state, is_promote
    ):
    if Good.query.filter(or_(
            Good.good_name == good_name)).first():
        return ValidationErrorResult(message='Good已存在')
    good = Good(
        good_name=good_name, good_state=good_state,
        good_price=good_price, good_number=good_number,
        good_weight=good_weight, good_desc=good_desc,
        hot_number=hot_number, is_promote=is_promote)

    category = Category.query.filter(Category.id == category_id).one()
    if category:
        category.goods.append(good)
        good.category_id = category_id
    if photos:
        for photo in photos:
            ph = Photo(photo_name=photo['photo_name'], photo_url=photo['photo_url'])
            good.photos.append(ph)
    if attributes:
        for attribute in attributes:
            attr = Attribute.query.filter(Attribute.id == attribute['id']).one()
            if attr:
                attr.attribute_values = attribute['attribute_values']
    db.session.add(good)
    db.session.flush()
    return jsonify(schemas.good_schema.dump(good)), 201


@bp.route('/goods/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve(pk):
    good = Good.query.filter(Good.id == pk).one()
    return jsonify(schemas.good_schema.dump(good)), 200


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


@bp.route('/goods/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete(pk):
    good = Good.query.filter(Good.id == pk).one()
    if not Good:
        return ValidationErrorResult(
            message='ID 为{pk} Good不存在')
    db.session.delete(good)
    db.session.flush()
    return '', 204


@bp.route('/categories/', methods=['GET'])
@use_kwargs(PageParams)
# @use_kwargs({'type': fields.List(fields.Integer(), required=False)})
@use_kwargs({'type': fields.Integer(required=False)})
@jwt_required()
def list_category(page, page_size, order_by, type=3):
    # qexp = Category.query.filter(Category.category_level.in_(range(type)))
    qexp = Category.query.filter(Category.category_level==type-1)
    paged_ret = pagination(Category, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_category_schemas.dump(paged_ret))


@bp.route('/categories/', methods=['POST'])
@use_kwargs(schemas.category_create_schema)
@jwt_required()
@transaction(db.session)
def create_category(category_name, category_level, category_desc, parent_id=None):
    if Category.query.filter(or_(
            Category.category_name == category_name)).first():
        return ValidationErrorResult(message='Category已存在')
    category = Category(
        category_name=category_name, category_level=category_level,
        category_desc=category_desc)
    # category = Category(
    #     category_name=category_name, category_level=category_level)
    if parent_id:
        parent = Category.query.filter_by(id=parent_id).one()
        if parent:
            parent.children.append(category)
            category.parent_id = parent_id
    db.session.add(category)
    db.session.flush()

    return jsonify(schemas.category_schema.dump(category)), 201


@bp.route('/categories/<int:pk>/', methods=['GET'])
@jwt_required()
def retrieve_category(pk):
    category = Category.query.filter(Category.id == pk).one()
    return jsonify(schemas.category_schema.dump(category)), 200


@bp.route('/categories/<int:pk>/children/', methods=['PUT'])
@use_kwargs({'children': fields.List(fields.Integer(), required=True)})
@jwt_required()
@transaction(db.session)
def update_children(children, pk):

    category = Category.query.filter(Category.id == pk).one()
    if not category:
        return ValidationErrorResult(
            message='ID 为{pk} 分类不存在')
    if children:
        categories = Category.query.filter(Category.id.in_(children)).all()
        category.children = categories
    db.session.flush()

    return jsonify(schemas.category_schema.dump(category)), 200


@bp.route('/categories/<int:pk>/', methods=['PUT'])
@use_kwargs(schemas.category_create_schema)
@jwt_required()
@transaction(db.session)
def update_category(category_name, category_level, pk, category_desc=''):

    category = Category.query.filter(Category.id == pk).one()
    if not category:
        return ValidationErrorResult(
            message='ID 为{pk} 分类不存在')
    category.category_name = category_name
    category.category_desc = category_desc
    category.category_level = category_level
    db.session.flush()

    return jsonify(schemas.category_schema.dump(category)), 200


@bp.route('/categories/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete_category(pk):
    category = Category.query.filter(Category.id == pk).one()
    if not category:
        return ValidationErrorResult(
            message='ID 为{pk} Category不存在')
    db.session.delete(category)
    db.session.flush()
    return '', 204


@bp.route('/attributes/', methods=['GET'])
@use_kwargs(PageParams)
# @use_kwargs({'type': fields.List(fields.Integer(), required=False)})
# @use_kwargs({'type': fields.Integer(required=False)})
@jwt_required()
def list_attribute(page, page_size, order_by):
    # qexp = Category.query.filter(Category.category_level.in_(range(type)))
    # qexp = Category.query.filter(Category.category_level==type-1)
    qexp = Attribute.query
    paged_ret = pagination(Attribute, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_attribute_schemas.dump(paged_ret))


@bp.route('/categories/<int:category_id>/attributes/', methods=['POST'])
@use_kwargs(schemas.attribute_create_schema)
@jwt_required()
@transaction(db.session)
def create_attribute(attribute_name, attribute_sel, attribute_write, category_id, attribute_values=None):
    # if Attribute.query.filter(or_(
    #         Attribute.attribute_name == attribute_name)).first():
    #     return ValidationErrorResult(message='Attribute已存在')
    attribute = Attribute(
        attribute_name=attribute_name, attribute_sel=attribute_sel,
        attribute_write=attribute_write, attribute_values=attribute_values)
    # category = Category(
    #     category_name=category_name, category_level=category_level)
    if category_id:
        category = Category.query.filter_by(id=category_id).one()
        if category:
            category.attributes.append(attribute)
            attribute.category_id = category_id
    db.session.add(attribute)
    db.session.flush()

    return jsonify(schemas.attribute_schema.dump(attribute)), 201


@bp.route('/categories/<int:category_id>/attributes/<int:attribute_id>/', methods=['GET'])
@jwt_required()
def retrieve_attributes(category_id, attribute_id):
    category = Category.query.filter(Category.id == category_id).one()
    attribute = category.attributes.filter_by(id=attribute_id).one()
    return jsonify(schemas.attribute_schema.dump(attribute)), 200


@bp.route('/attributes/<int:attribute_id>/', methods=['PUT'])
@jwt_required()
@use_kwargs(schemas.attribute_create_schema)
@transaction(db.session)
def update_attribute(attribute_id, attribute_name, attribute_sel, attribute_write, attribute_values):
    attribute = Attribute.query.filter(Attribute.id == attribute_id).one()
    if not attribute:
        return ValidationErrorResult(
            message='ID 为{attribute} 属性不存在')
    attribute.attribute_name = attribute_name
    attribute.attribute_sel = attribute_sel
    attribute.attribute_write = attribute_write
    attribute.attribute_values = attribute_values
    db.session.flush()
    return jsonify(schemas.attribute_schema.dump(attribute)), 200


@bp.route('/attributes/<int:pk>/', methods=['DELETE'])
@jwt_required()
@transaction(db.session)
def delete_attribute(pk):
    attribute = Attribute.query.filter(Attribute.id == pk).one()
    if not attribute:
        return ValidationErrorResult(
            message='ID 为{pk} Attribute不存在')
    db.session.delete(attribute)
    db.session.flush()
    return '', 204


@bp.route('/categories/<int:pk>/attributes/', methods=['GET'])
@use_kwargs(PageParams)
# @use_kwargs({'type': fields.List(fields.Integer(), required=False)})
@use_kwargs({'attribute_sel': fields.String(required=False)})
@jwt_required()
def category_attributes(pk, page, page_size, order_by, attribute_sel=None):
    category = Category.query.filter_by(id=pk).one()
    if not category:
        return ValidationErrorResult(message='ID 为{pk} 分类不存在')
    qexp = category.attributes.filter(Attribute.attribute_sel == attribute_sel)
    # qexp = Category.query.filter(Category.category_level.in_(range(type)))
    paged_ret = pagination(Attribute, page, page_size, order_by, query_exp=qexp)
    return jsonify(schemas.paged_attribute_schemas.dump(paged_ret))


@bp.route('/goods/upload/', methods=['POST'])
@jwt_required()
# @use_kwargs({'type': fields.List(fields.Integer(), required=False)})
@use_kwargs({'photo': fields.Field(required=True, location='files')})
def uploads(photo):
    photo_name = photos.save(photo)
    photo_url = photos.url(photo_name)
    return jsonify({
        'photo_url': photo_url,
        'photo_name': photo_name
    })
