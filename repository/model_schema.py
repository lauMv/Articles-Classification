from marshmallow import Schema, fields, EXCLUDE


class ArticleSchema(Schema):
    min_df = fields.Int(allow_none=False)
    max_features = fields.Int(allow_none=False)
    model_path = fields.Str(allow_none=False)
    model_accuracy = fields.Float(allow_none=False)
    model_precision = fields.Float(allow_none=False)
    model_recall = fields.Float(allow_none=False)
    model_f1 = fields.Float(allow_none=False)
    class Meta:
        unknown = EXCLUDE
