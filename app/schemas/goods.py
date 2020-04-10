from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import Good, Category


class GoodSchema(ModelSchema):
    # good_name = fields.Str(required=True, dump_only=True)
    good_name = fields.Str(required=True)
    good_price = fields.Number(required=True)
    good_number = fields.Number(required=True)
    # category = fields.Nested('self', many=True)

    class Meta:
        model = Good
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'good_name', 'good_price', 'good_number'
        )
        load_only = ()
        dump_only = ()


class PagedGoodSchema(PagedSchema):
    items = fields.Nested(GoodSchema, many=True, exclude=[])


class GoodCreateSchema(ModelSchema):
    # good_name = fields.Str(required=True, dump_only=True)
    good_name = fields.Str(required=True)
    good_price = fields.Number(required=True)
    good_number = fields.Number(required=True)
    good_state = fields.Boolean(required=True)

    class Meta(GoodSchema.Meta):
        model = Good
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'good_name', 'good_price', 'good_number', 'good_state', 'good_state'
        )
        dump_only = tuple(set(fields) - {'good_name', 'good_price', 'good_number', 'good_state'})


class CategorySchema(ModelSchema):
    # category_name = fields.Str(dump_only=True)
    category_name = fields.Str(required=True)
    category_desc = fields.Str(required=False)
    category_level = fields.Number(required=True)
    # children = fields.Nested('self', many=True, exclude=['children'])
    # children_f = fields.Nested('self', many=True, exclude=['children'])
    children = fields.Nested('self', many=True)
    children_f = fields.Nested('self', many=True)

    class Meta:
        model = Good
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'children_f',
            'category_name', 'category_level', 'children', 'category_desc'
        )
        load_only = ()
        dump_only = ()


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


good_schema = GoodSchema()
paged_good_schemas = PagedGoodSchema()
good_create_schema = GoodCreateSchema()

category_schema = CategorySchema()
paged_category_schemas = PagedCategorySchema()
category_create_schema = CategoryCreateSchema()
