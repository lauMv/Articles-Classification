# This Python file uses the following encoding: utf-8
import pickle
from datetime import datetime
from repository import article_db, classifier_db
import os

from text_classifier.model import Model


class Classifier:

    def __init__(self):
        self.model = Model()

    def train_model_local(self, version, conflict_words, x_train, y_train, test_docs, test_docs_class):
        mod, doc_vec = self.model.initial_function(x_train, conflict_words)
        self.model.vectorizer = mod
        mod = self.model.fit(doc_vec, y_train)
        self.model.clf = mod
        mod = self.model.fit(test_docs, test_docs_class)
        self.model.clf = mod
        predicted = self.model.predict(test_docs, test_docs_class, False, conflict_words)
        self.model.eval_model(test_docs_class, predicted)
        classifier = {
            "version": version + 1,
            "model_path": "classifiers/",
            "model_accuracy": self.model.accuracy,
            "model_precision": self.model.precision,
            "model_recall": self.model.recall,
            "model_f1": self.model.f1,
            "creation_date": datetime.date.today(),
            "is_in_use": True}
        classifier_db.create(self.model)
        print("clasificador entrenado satisfactoriamente: ")
        with open('classifiers/model{0}.pkl'.format(version+1), 'wb') as f:
            pickle.dump(self.model, f)

    def train_model(self, version, conflict_words):
        x_train = article_db.get_by_user_classification(False)
        y_train = article_db.get_by_user_classification(True)
        docs_class = [0 for elem in range(0, len(x_train))] + [0 for elem in range(0, len(y_train))]
        doc_vec = self.model.fit(x_train + y_train, docs_class, True, conflict_words)
        predicted_class = self.model.predict(doc_vec)
        self.model.eval_model(docs_class, predicted_class)
        classifier = {
            "version": version + 1,
            "model_path": "classifiers/",
            "model_accuracy": self.model.accuracy,
            "model_precision": self.model.precision,
            "model_recall": self.model.recall,
            "model_f1": self.model.f1,
            "creation_date": datetime.date.today(),
            "is_in_use": True}
        classifier_db.create(self.model)
        print("Clasificador entrenado satisfactoriamente: ")
        with open('classifiers/model{0}.pkl'.format(version+1), 'wb') as f:
            pickle.dump(self.model, f)

    def predict(self, doc_file):
        doc_vec = self.model.fit(doc_file)
        return self.predict(doc_vec)

    def evaluate(self, expected, predicted):
        print(self.model.eval_model(expected, predicted))

    def save_model_classification(self, predicted, data):

        def save_classification_db(filename, classification):
            source_file_path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", filename)
            id = article_db.get_id(source_file_path)
            try:
                if classification.astype(int) == 1:
                    update = {
                        "model_classification": True}
                    article_db.update(update, id)
                    print("Update:", source_file_path)
            except:
                print("no guardo")
                pass

        article_classification = [(data[i], predicted[i]) for i in
                                  range(0, len(data))]
        for article in article_classification:
            print(article[0], article[1])
            save_classification_db(article[0], article[1])

    def print_eval(self):
        print('accurancy: ', self.model.accuracy)
        print('precision: ', self.model.precision)
        print('reca;;: ', self.model.recall)
        print('f1: ', self.model.f1)
        pass


if __name__ == '__main__':
    classifier = Classifier()