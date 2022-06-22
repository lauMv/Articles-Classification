from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from repository import article_db
from repository import classifier_db

class Model():

    def __init__(self):
        self.clf = LogisticRegression()
        self.vectorizer = CountVectorizer(encoding='utf-8', min_df=0.1, max_features=634)
        self.flags = []
        self.accuracy = 0
        self.precision = 0
        self.recall = 0
        self.f1 = 0

    def fit_transform(self, pre_process_docs):
        pre_process_docs = self.vectorizer.transform(pre_process_docs)
        return pre_process_docs

    def fit(self, pre_processes_docs, pre_processes_docs_class):
        # if not self.flags:
        #     self.vectorizer.fit(pre_processes_docs)
        # else:
        #     self.vectorizer.fit(pre_processes_docs, self.flags)
        #
        # pre_processes_docs_vec = self.fit_transform(pre_processes_docs)
        # self.clf.fit(pre_processes_docs_vec.toarray(), pre_processes_docs_class)
        pre_processes_docs = self.vectorizer.fit_transform(pre_processes_docs)
        self.clf.fit(pre_processes_docs, pre_processes_docs_class)

    def predict(self, pre_processes_docs_vec):
        new_pre_processes_docs_predicted_class = self.clf.predict(pre_processes_docs_vec)
        return new_pre_processes_docs_predicted_class


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


    def save_model_to_db(self):
        classifier = {
            "version": "",
            "model_path": "",
            "model_accuracy": self.accuracy,
            "model_precision": self.precision,
            "model_recall": self.recall,
            "model_f1": self.f1,
            "creation_date": "",
            "is_in_use": False
        }
        classifier_db.create(classifier)

def train_model():
    non_conflict_articles = article_db.get_by_user_classification('False')
    conflict_articles = article_db.get_by_user_classification('True')

    # pre_processes_docs, pre_processes_docs_vect = test_model()
    # predicted = predict_articles(model, pre_processes_docs)
    # expected = list(0 for elem in range(0, 35)) + list(1 for elem in range(0, 35))
    # model.eval_model(expected, predicted)

#
# def get_articles_by_name(filename)
#     def test_model():
#         pre_processes_docs = get_articles("test_articles", "buenos")
#         pre_processes_docs_class = [0 for article in pre_processes_docs]
#         pre_processes_conflicts_docs = get_articles("test_articles", "malos")
#         pre_processes_conflicts_docs_class = [1 for article in pre_processes_docs]
#
#         pre_processes_docs = pre_processes_docs + pre_processes_conflicts_docs
#         pre_processes_docs_class = pre_processes_docs_class + pre_processes_conflicts_docs_class
#         return pre_processes_docs, pre_processes_docs_class
#
