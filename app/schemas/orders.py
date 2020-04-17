import logging

from marshmallow import fields
from hobbit_core.schemas import PagedSchema, ModelSchema

from app.models import Order


class OrderSchema(ModelSchema):
    # good_name = fields.Str(required=True, dump_only=True)
    order_number = fields.Str(required=True)
    trad_no = fields.Str(required=False, default='')
    invoice_titile = fields.Str(required=False, default='')
    invoice_company = fields.Str(required=False, default='')
    invoice_content = fields.Str(required=False, default='')
    consignee_address = fields.Str(required=False, default='')
    order_price = fields.Number(required=True, default=0.0)
    pay_status = fields.Str(required=False, default='未支付')
    is_send = fields.Boolean(required=False, default=False)

    user = fields.Nested('UserSchema', only=('id', 'username'))
    goods = fields.Nested('GoodSchema', many=True)


    class Meta:
        model = Order
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'order_number',
            'trad_no', 'invoice_titile', 'invoice_company',
            'invoice_content', 'is_send', 'user', 'goods',
            'consignee_address', 'order_price', 'pay_status'
        )
        load_only = ()
        dump_only = ()


class PagedOrderSchema(PagedSchema):
    items = fields.Nested(OrderSchema, many=True, exclude=[])


class OrderCreateSchema(ModelSchema):
    order_number = fields.Str(required=True)
    trad_no = fields.Str(required=False, default='')
    invoice_titile = fields.Str(required=False, default='')
    invoice_company = fields.Str(required=False, default='')
    invoice_content = fields.Str(required=False, default='')
    consignee_address = fields.Str(required=False, default='')
    order_price = fields.Number(required=True, default=0.0)
    pay_status = fields.Str(required=False, default='未支付')
    is_send = fields.Boolean(required=False, default=False)
    user_id = fields.Int(required=True)
    goods = fields.List(fields.Dict(), required=True)

    class Meta(OrderSchema.Meta):
        model = Order
        strict = True
        fields = (
            'id', 'created_at', 'updated_at', 'order_number',
            'trad_no', 'invoice_titile', 'invoice_company',
            'invoice_content', 'is_send', 'user_id', 'goods',
            'consignee_address', 'order_price', 'pay_status'
        )
        # dump_only = tuple(set(fields) - {'good_name', 'good_price', 'good_number', 'good_state'})


order_schema = OrderSchema()
paged_order_schemas = PagedOrderSchema()
order_create_schema = OrderCreateSchema()