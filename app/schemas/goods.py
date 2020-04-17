import logging

from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import Good, Category, Attribute


class GoodSchema(ModelSchema):
    # good_name = fields.Str(required=True, dump_only=True)
    good_name = fields.Str(required=True)
    good_desc = fields.Str(required=False, default='')
    good_price = fields.Number(required=True, default=0.0)
    good_weight = fields.Number(required=True, default=0.0)
    good_number = fields.Integer(required=True, default=0)
    hot_number = fields.Integer(required=False, default=0)
    good_state = fields.Str(required=False, default='审核中')
    is_promote = fields.Boolean(required=False, default=False)
    # category = fields.Nested('self', many=True)

    class Meta:
        model = Good
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'good_desc',
            'good_name', 'good_price', 'good_number', 'good_weight',
            'hot_number', 'good_state', 'is_promote'
        )
        load_only = ()
        dump_only = ()


class PagedGoodSchema(PagedSchema):
    items = fields.Nested(GoodSchema, many=True, exclude=[])


class GoodCreateSchema(ModelSchema):
    # good_name = fields.Str(required=True, dump_only=True)
    good_name = fields.Str(required=True)
    good_price = fields.Number(required=False, missing=0.0)
    good_number = fields.Number(required=False, missing=0)
    good_state = fields.Str(required=False, missing='审核中')
    good_weight = fields.Number(required=False, missing=0.0)
    good_desc = fields.Str(required=False, default='')
    category_id = fields.Int(required=True)
    photos = fields.List(fields.Dict(), required=False, missing=[])
    attributes = fields.List(fields.Dict(), required=False, missing=[])
    hot_number = fields.Integer(required=False, default=0)
    is_promote = fields.Boolean(required=False, default=False)

    class Meta(GoodSchema.Meta):
        model = Good
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'good_weight',
            'category_id', 'photos', 'attributes', 'good_name',
            'good_price', 'good_number', 'good_state', 'good_state',
            'good_desc', 'hot_number', 'is_promote'
        )
        # dump_only = tuple(set(fields) - {'good_name', 'good_price', 'good_number', 'good_state'})


class CategorySchema(ModelSchema):
    # category_name = fields.Str(dump_only=True)
    category_name = fields.Str(required=True)
    category_desc = fields.Str(required=False)
    category_level = fields.Number(required=True)
    # children = fields.Nested('self', many=True, exclude=['children'])
    # children_f = fields.Nested('self', many=True, exclude=['children'])
    children = fields.Nested('self', many=True)
    # TODO: 优化自引用过滤
    children_f = fields.Nested('self', many=True)
    children_p = fields.Nested('self', many=True)
    attributes = fields.Nested('AttributeSchema', many=True, only=['attribute_name', 'attribute_values'])
    # name = fields.Method('get_children')

    class Meta:
        model = Category
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'children_f', 'children_p',
            'category_name', 'category_level', 'children', 'category_desc', 'attributes'
        )
        load_only = ()
        dump_only = ()

    # def get_children(self, obj):
    #     logging.error((type(obj), dir(obj), obj))
    #     return obj.children


class PagedCategorySchema(PagedSchema):
    items = fields.Nested(CategorySchema, many=True, exclude=[])


class CategoryCreateSchema(ModelSchema):
    # category_name = fields.Str(dump_only=True)
    category_name = fields.Str(required=True)
    category_desc = fields.Str(required=False)
    category_level = fields.Number(required=True)
    parent_id = fields.Number(required=False, default=None)

    class Meta(GoodSchema.Meta):
        model = Good
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'category_name', 'category_level', 'category_desc', 'parent_id'
        )
        dump_only = tuple(set(fields) - {'category_name', 'category_level', 'category_desc', 'parent_id'})


class AttributeSchema(ModelSchema):
    attribute_name = fields.Str(required=True)
    attribute_sel = fields.Str(required=False)
    attribute_values = fields.Str(required=False)
    attribute_write = fields.Str(required=False)

    class Meta:
        model = Attribute
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'attribute_name', 'attribute_sel',
            'attribute_values', 'attribute_write'
        )
        load_only = ()
        dump_only = ()

    # def get_children(self, obj):
    #     logging.error((type(obj), dir(obj), obj))
    #     return obj.children


class PagedAttributeSchema(PagedSchema):
    items = fields.Nested(AttributeSchema, many=True, exclude=[])


class AttributeCreateSchema(ModelSchema):
    attribute_name = fields.Str(required=True)
    attribute_sel = fields.Str(required=False)
    attribute_values = fields.Str(required=False)
    attribute_write = fields.Str(required=False)
    # category_id = fields.Number(required=False, default=None)

    class Meta(GoodSchema.Meta):
        model = Attribute
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'attribute_name', 'attribute_sel',
            'attribute_values', 'attribute_write'
        )
        dump_only = tuple(
            set(fields) - {
                'attribute_name', 'attribute_sel',
                'attribute_values', 'category_id',
                'attribute_write'})


good_schema = GoodSchema()
paged_good_schemas = PagedGoodSchema()
good_create_schema = GoodCreateSchema()

category_schema = CategorySchema()
paged_category_schemas = PagedCategorySchema()
category_create_schema = CategoryCreateSchema()

attribute_schema = AttributeSchema()
paged_attribute_schemas = PagedAttributeSchema()
attribute_create_schema = AttributeCreateSchema()