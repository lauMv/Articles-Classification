from marshmallow import Schema, fields, EXCLUDE


class HeuristicSchema(Schema):
    word = fields.Str(allow_none=True)
    type = fields.Boolean(allow_none=False)

    class Meta:
        unknown = EXCLUDE
