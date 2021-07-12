from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError
import db
from articles_schema import ArticleSchema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.before_first_request
def initialize_database():
    db.initialize()

class Articles(Resource):
    def get(self, Id=None):
        if Id is None:
            return db.get_all()

        article = db.get(Id)
        if not article:
            abort(404, errors={"errors": {"message": "Article with Id {} does not exist".format(Id)}})
        return article

    def post(self):
        try:
            article = ArticleSchema(exclude=["id"]).loads(request.json)
            if not db.create(article):
                abort(404, errors={"errors": {"message": "Article with name {} already exists".format(request.json["source_file_path"])}})
        except ValidationError as e:
            abort(405, errors=e.messages)


api.add_resource(Articles, "/articles", "/articles/<int:Id>")

if __name__ == "__main__":
    app.run(host="192.168.0.55")
