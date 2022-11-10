from dataclasses import field
from marshmallow import Schema, fields

class Token(Schema):
    token_type = fields.String()
    exp = fields.Number()
    jti = fields.String()
    user_id = fields.Number()