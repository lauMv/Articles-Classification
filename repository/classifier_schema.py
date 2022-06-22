from marshmallow import Schema, fields, EXCLUDE


class ClassifierSchema(Schema):
    version = fields.Str(allow_none=False)
    model_path = fields.Str(allow_none=False)
    model_accuracy = fields.Float(allow_none=False)
    model_precision = fields.Float(allow_none=False)
    model_recall = fields.Float(allow_none=False)
    model_f1 = fields.Float(allow_none=False)
    creation_date = fields.Date(allow_none=False)
    is_in_use = fields.Boolean(allow_none=True)

    class Meta:
        unknown = EXCLUDE
