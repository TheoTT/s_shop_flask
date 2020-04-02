from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import Role


class RoleSchema(ModelSchema):
    role_name = fields.Str(required=True)
    role_desc = fields.Str(required=False)
    users = fields.Nested('UserSchema', many=True, only=['id', 'username'])
    # menus = fields.Nested('MenuSchema', many=True, only=['id', 'auth_name', 'children'])
    role_menus = fields.Nested('MenuSchema', many=True, only=['id', 'auth_name', 'children'])
    # role = fields.Dict(values=fields.Str(), keys=fields.Str(), dump_only=True)
    
    class Meta:
        model = Role
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'role_name', 'users', 'role_menus', 'role_desc', 'menus'
        )
        load_only = ()
        dump_only = ()


class RoleModSchema(ModelSchema):
    role_name = fields.Str(required=True)
    role_desc = fields.Str(required=False)
    menu_ids = fields.List(fields.Integer(), required=False)
    # role = fields.Dict(values=fields.Str(), keys=fields.Str(), dump_only=True)

    class Meta:
        model = Role
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'role_name', 'role_desc', 'menu_ids'
        )
        load_only = ()
        dump_only = ()


class PagedRoleSchema(PagedSchema):
    items = fields.Nested(RoleSchema, many=True, exclude=[])


role_schema = RoleSchema(exclude=[])
role_mod_schema = RoleModSchema()
paged_role_schemas = PagedRoleSchema()
