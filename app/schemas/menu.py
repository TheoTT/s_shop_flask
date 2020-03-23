from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import Menu


class MenuSchema(ModelSchema):
    auth_name = fields.Str(dump_only=True)
    path = fields.Str(required=True)
    # children = fields.Nested(SubMenuSchema)

    class Meta:
        model = Menu
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'auth_name', 'path', 'sub_menu',
        )
        load_only = ()
        dump_only = ()

# class SubMenuSchema(ModelSchema):
#     child = fields.Nested(MenuSchema)
#     parent = fields.Nested(MenuSchema)


class PagedMenuSchema(PagedSchema):
    items = fields.Nested(MenuSchema, many=True, exclude=[])


class MenuCreateSchema(ModelSchema):
    auth_name = fields.Str(required=True)
    path = fields.Str(required=True, validate=lambda x: len(x) >= 1)
    child_id = fields.Int(required=False, default=None)
    parent_id = fields.Int(required=False, default=None)

    class Meta(MenuSchema.Meta):
        model = Menu
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'auth_name', 'path', 'child_id', 'parent_id'
        )
        dump_only = tuple(set(fields) - {'auth_name', 'path', 'child_id', 'parent_id'})


menu_schema = MenuSchema()
paged_menu_schemas = PagedMenuSchema()
menu_create_schema = MenuCreateSchema()