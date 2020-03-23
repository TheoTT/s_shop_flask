from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import Menu, SubMenu


class SubMenuSchema(ModelSchema):
    auth_name = fields.Str(dump_only=True)
    path = fields.Str(required=True)

    class Meta:
        model = SubMenu
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'auth_name', 'path'
        )
        load_only = ()
        dump_only = ()


class MenuSchema(ModelSchema):
    auth_name = fields.Str(dump_only=True)
    path = fields.Str(required=True)
    children = fields.Nested(SubMenuSchema, many=True)

    class Meta:
        model = Menu
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'auth_name', 'path', 'children',
        )
        load_only = ()
        dump_only = ()


class PagedMenuSchema(PagedSchema):
    items = fields.Nested(MenuSchema, many=True, exclude=[])


class PagedSubMenuSchema(PagedSchema):
    items = fields.Nested(SubMenuSchema, many=True, exclude=[])


class MenuCreateSchema(ModelSchema):
    auth_name = fields.Str(required=True)
    path = fields.Str(required=True, validate=lambda x: len(x) >= 1)
    child_id = fields.Int(required=False, default=None)

    class Meta(MenuSchema.Meta):
        model = Menu
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'auth_name', 'path', 'child_id'
        )
        dump_only = tuple(set(fields) - {'auth_name', 'path', 'child_id'})


class SubMenuCreateSchema(ModelSchema):
    auth_name = fields.Str(required=True)
    path = fields.Str(required=True, validate=lambda x: len(x) >= 1)

    class Meta(MenuSchema.Meta):
        model = SubMenu
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'auth_name', 'path', 'child_id'
        )
        dump_only = tuple(set(fields) - {'auth_name', 'path'})


menu_schema = MenuSchema()
paged_menu_schemas = PagedMenuSchema()
menu_create_schema = MenuCreateSchema()

sub_menu_schema = SubMenuSchema()
paged_sub_menu_schemas = PagedSubMenuSchema()
sub_menu_create_schema = SubMenuCreateSchema()