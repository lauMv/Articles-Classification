import datetime
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from repository import article_db, classifier_db
from repository import heuristic_db


def flags_words(list_docs):
    flags = []

    def count_words(article):
        cant = 0
        for word in article.split(' '):
            if word in heuristic_db.get_conflict_words():
                cant = cant + 1
            if word in heuristic_db.get_save_words():
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

    def set_vectorizer_function(self, docs, conflict_words):
        if conflict_words:
            self.vectorizer = self.vectorizer.fit(docs, flags_words(docs))
        else:
            self.vectorizer = self.vectorizer.fit(docs)
        doc_vec = self.vectorizer.transform(docs)
        return doc_vec.toarray()

    def fit(self, doc_vec, docs_class):
        return self.clf.fit(doc_vec, docs_class)
        # return model

    def predict(self, docs):
        doc_vec = self.vectorizer.transform(docs)
        return self.clf.predict(doc_vec)

    def eval_model(self, expected_val, predicted_val):
        self.accuracy = round(accuracy_score(expected_val, predicted_val), 2)
        self.precision = round(precision_score(expected_val, predicted_val), 2)
        self.recall = round(recall_score(expected_val, predicted_val), 2)
        self.f1 = round(f1_score(expected_val, predicted_val), 2)
        print('accuracy del clasificador {0:.2f}'.format(self.accuracy))
        print('confusion matrix:', confusion_matrix(expected_val, predicted_val))
        print('precision del clasificador {0:.2f}'.format(self.precision))
        print('recall del clasificador - version 1 : {0:.2f}'.format(self.recall))
        print('f1 del clasificador - version 1 : {0:.2f}'.format(self.f1))

    def show_metricts(self):
        print('accuracy del clasificador {0:.2f}'.format(self.accuracy))
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

    def save_model_classification(self, predicted, data):

        def save_classification_db(filename, classification):
            try:
                if classification.astype(int) == 1:
                    update = {
                        "model_classification": True}
                    article_db.update(update, filename)
                    print("Update:", filename)
            except:
                print("no guardo")
                pass

        article_classification = [(data[i], predicted[i]) for i in
                                  range(0, len(data))]
        for article in article_classification:
            print(article[0], article[1])
            save_classification_db(article[0], article[1])


def train_model(conflict_words, x_train, y_train, test_docs, test_docs_class):
    model = Model()
    x_train = model.set_vectorizer_function(x_train, conflict_words)
    model.fit(x_train, y_train)
    predicted_class = model.predict(test_docs)
    version = classifier_db.get_cant_classifier()
    version = version[0].get('count')
    classifier_db.update_state(version)
    model.eval_model(test_docs_class, predicted_class)
    classifier = {
        'version': version + 1,
        'model_path': "classifiers/",
        'model_accuracy': model.accuracy,
        'model_precision': model.precision,
        'model_recall': model.recall,
        'model_f1': model.f1,
        'creation_date': datetime.date.today(),
        'is_in_use': True}
    classifier_db.create(classifier)
    print("save classifier into DB")
    with open('./text_classifier/classifiers/model_{0}.pkl'.format(version+1), 'wb') as f:
        pickle.dump(model, f)
# if __name__ == '__main__':
#     M = Model()