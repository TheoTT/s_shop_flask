from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import User


class UserSchema(ModelSchema):
    token = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email()
    # role = fields.Dict(values=fields.Str(), keys=fields.Str(), dump_only=True)
    role = fields.Nested('RoleSchema', only=['role_name', 'role_desc'])

    class Meta:
        model = User
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'username', 'password', 'token', 'del_flag', 'status', 'email', 'role'
        )
        load_only = ('password', )
        dump_only = ('token')


class PagedUserSchema(PagedSchema):
    items = fields.Nested(UserSchema, many=True, exclude=['token'])


class UserCreateSchema(ModelSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    email = fields.Email(required=True)

    class Meta(UserSchema.Meta):
        model = User
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'username', 'password', 'status', 'email'
        )
        dump_only = tuple(set(fields) - {'username', 'password', 'email'})


class UserModSchema(ModelSchema):
    username = fields.Str(required=True)
    # password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    email = fields.Email(required=True)
    # role_id = fields.Number(required=False)

    class Meta:
        model = User
        strict = True
        fields = (
            'id', 'created_at', 'updated_at',
            'username', 'email'
        )
        dump_only = tuple(set(fields) - {'username', 'email'})


token_schema = UserSchema()
user_schema = UserSchema(exclude=['token'])
paged_user_schemas = PagedUserSchema()
user_create_schema = UserCreateSchema()
user_mod_schema = UserModSchema()