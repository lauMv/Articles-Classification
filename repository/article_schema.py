from marshmallow import Schema, fields, EXCLUDE


class ArticleSchema(Schema):
    source_file_path = fields.Str(allow_none=False)
    pre_processed_file_path = fields.Str(allow_none=True)
    filename = fields.Str(allow_none=False)
    extraction_date = fields.Date(allow_none=True)
    paper = fields.Str(allow_none=False)
    article_content = fields.Str(allow_none=False)
    user_classification = fields.Str(allow_none=True)
    model_classification = fields.Boolean(allow_none=True)
    used_in_classifier = fields.Boolean(allow_none=True)

    class Meta:
        unknown = EXCLUDE