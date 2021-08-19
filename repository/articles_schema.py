from marshmallow import Schema, fields, EXCLUDE


# FIXME actualizar el esquema emparejando adecuadamente los tipos de datos
class ArticleSchema(Schema):
    source_file_path = fields.Str(allow_none=False)
    pre_processed_file_path = fields.Str(allow_none=False)
    extraction_date = fields.Str(allow_none=False)              # FIXME actualizar
    user_classification = fields.Str(allow_none=True)           # FIXME actualizar
    model_classification = fields.Str(allow_none=True)          # FIXME actualizar

    class Meta:
        unknown = EXCLUDE
