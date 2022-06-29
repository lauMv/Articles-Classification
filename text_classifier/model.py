import datetime
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from repository import article_db
from repository import classifier_db


def flags_words(list_docs):
    flags = []

    def count_words(article):
        cant = 0
        for word in article.split(' '):
            if word in classifier_db.get_conflict_word():
                cant = cant + 1
            if word in classifier_db.get_save_words():
                cant = cant - 1
        return cant

    for article in list_docs:
        flags.append(count_words(article))
    return flags


class Model:

    def __init__(self):
        self.clf = LogisticRegression()
        self.vectorizer = CountVectorizer(encoding='utf-8', min_df=0.1, max_features=634)
        self.accuracy = 0
        self.precision = 0
        self.recall = 0
        self.f1 = 0
        self.version = 0

    def initial_function(self, docs, extra):
        if extra:
            self.vectorizer = self.vectorizer.fit(docs, flags_words(docs))
        else:
            self.vectorizer = self.vectorizer.fit(docs)
        doc_vec = self.vectorizer.transform(docs)
        model = self.vectorizer
        return model, doc_vec.toarray()

    def fit(self, doc_vec, docs_class):
        model = self.clf.fit(doc_vec, docs_class)
        return model


    def predict(self, doc_vec):
        doc_vec = self.vectorizer.transform(doc_vec)
        return self.clf.predict(doc_vec)

    def eval_model(self, expected_val, predicted_val):
        self.accuracy = accuracy_score(expected_val, predicted_val)
        self.precision = precision_score(expected_val, predicted_val)
        self.recall = recall_score(expected_val, predicted_val)
        self.f1 = f1_score(expected_val, predicted_val)
        print('accuracy del clasificador {0:.2f}'.format(self.accuracy))
        print('confusion matrix:', confusion_matrix(expected_val, predicted_val))
        print('precision del clasificador {0:.2f}'.format(self.precision))
        print('recall del clasificador - version 1 : {0:.2f}'.format(self.recall))
        print('f1 del clasificador - version 1 : {0:.2f}'.format(self.f1))

    def update_eval_model_to_db(self):
        classifier = {
            "model_accuracy": self.accuracy,
            "model_precision": self.precision,
            "model_recall": self.recall,
            "model_f1": self.f1,
            "is_in_use": True
        }
        classifier_db.update(self.version)


def train_model(version, conflict_words, x_train, y_train):
    model = Model()
    docs_class = [0 for elem in range(0, len(x_train))] + [0 for elem in range(0, len(y_train))]
    doc_vec = model.fit(x_train + y_train, docs_class, True, conflict_words)
    predicted_class = model.predict(doc_vec)
    model.eval_model(docs_class, predicted_class)
    classifier = {
        "version": version + 1,
        "model_path": "classifiers/",
        "model_accuracy": model.accuracy,
        "model_precision": model.precision,
        "model_recall": model.recall,
        "model_f1": model.f1,
        "creation_date": datetime.date.today(),
        "is_in_use": True}
    classifier_db.create(model)
    with open('classifiers/model{0}.pkl'.format(version+1), 'wb') as f:
        pickle.dump(model, f)

# if __name__ == '__main__':
#     M = Model()