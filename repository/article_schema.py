from marshmallow import Schema, fields, EXCLUDE


class ArticleSchema(Schema):
    source_file_path = fields.Str(allow_none=False)
    pre_processed_file_path = fields.Str(allow_none=False)
    extraction_date = fields.Date(allow_none=False)
    user_classification = fields.Boolean(allow_none=False)
    model_classification = fields.Boolean(allow_none=False)

    class Meta:
        unknown = EXCLUDE
