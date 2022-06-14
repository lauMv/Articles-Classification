from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError
from flask_cors import CORS
from repository import db
from article_schema import ArticleSchema

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.before_first_request
def initialize_database():
    db.initialize()


class Article(Resource):
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
                abort(404, errors={"errors": {"message": "Article with title {} already exists".format(request.json["title"])}})
        except ValidationError as e:
            abort(405, errors=e.messages)

    def put(self, Id):
        try:
            article = ArticleSchema(exclude=["id"]).loads(request.json)
            if not db.update(article, Id):
                abort(404, errors={"errors": {"message": "Article with Id {} does not exist".format(Id)}})
        except ValidationError as e:
            abort(405, errors=e.messages)

    def delete(self, Id):
        if not db.delete(Id):
            abort(404, errors={"errors": {"message": "Article with Id {} does not exist".format(Id)}})


api.add_resource(Article, "/articles", "/articles/<int:Id>")

if __name__ == "__main__":
    app.run(host="localhost:5000")
