from marshmallow import Schema, fields, EXCLUDE

class ArticleSchema(Schema):
    id = fields.Integer(allow_none=True)
    name = fields.Str(required=True, error_messages={"required": "An exoplanet needs at least a name"})
    year_discovered = fields.Integer(allow_none=True)
    light_years = fields.Float(allow_none=True)
    mass = fields.Float(allow_none=True)
    link = fields.Url(allow_none=True)
    class Meta:
        unknown = EXCLUDE