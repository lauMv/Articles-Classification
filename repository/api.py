from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError
from flask_cors import CORS
from repository import article_db
from article_schema import ArticleSchema
from repository import classifier_db
from classifier_schema import ClassifierSchema

app = Flask(__name__)
# CORS(app)
api = Api(app)


@app.before_first_request
def initialize_database():
    article_db.init_db()


class Article(Resource):

    def get(self, Id=None):
        if Id is None:
            return article_db.get_all()

        article = article_db.get(Id)
        if not article:
            abort(404, errors={"errors": {"message": "Article with Id {} does not exist".format(Id)}})
        return article

    def post(self):
        try:
            article = ArticleSchema(exclude=["id"]).dumps(request.json)
            if not article_db.create(article):
                abort(404, errors={"errors": {"message": "Article with title {} already exists".format(request.json["filename"])}})
        except ValidationError as e:
            abort(405, errors=e.messages)

    def put(self, Id):
        try:
            article = ArticleSchema(exclude=["id"]).loads(request.json)
            if not article_db.update(article, Id):
                abort(404, errors={"errors": {"message": "Article with Id {} does not exist".format(Id)}})
        except ValidationError as e:
            abort(405, errors=e.messages)

    def delete(self, Id):
        if not article_db.delete(Id):
            abort(404, errors={"errors": {"message": "Article with Id {} does not exist".format(Id)}})


class Classifier(Resource):

    def get(self, Id=None):
        if Id is None:
            return classifier_db.get_all()

        classifier = classifier_db.get(Id)
        if not classifier:
            abort(404, errors={"errors": {"message": "classifier with Id {} does not exist".format(Id)}})
        return classifier

    def post(self):
        try:
            classifier = ClassifierSchema(exclude=["id"]).loads(request.json)
            if not classifier_db.create(classifier):
                abort(404, errors={"errors": {"message": "classifier with version {} already exists".format(request.json["version"])}})
        except ValidationError as e:
            abort(405, errors=e.messages)

    def put(self, Id):
        try:
            classifier = ClassifierSchema(exclude=["id"]).loads(request.json)
            if not classifier_db.update(classifier, Id):
                abort(404, errors={"errors": {"message": "classifier with Id {} does not exist".format(Id)}})
        except ValidationError as e:
            abort(405, errors=e.messages)


api.add_resource(Article, "/articles", "/articles/<int:Id>")
api.add_resource(Classifier, "/config")

if __name__ == "__main__":
    app.run(host="127.0.0.1")
