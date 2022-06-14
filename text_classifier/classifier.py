import re
from datetime import datetime
from pathlib import PurePosixPath

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from repository import db

import os


def execute():
    print("clasificando...")
    clf, count_vectorizer = train_classifier()
    classifier_articles(clf, count_vectorizer)


def upload_files_to_train():
    pre_processes_docs = [article for article in os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") +
                                                                         "articulos_pre_clasificados" + "\\" + "buenos_limpios"))]
    pre_processes_docs_class = [0 for article in pre_processes_docs]

    pre_processes_conflicts_docs = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articulos_pre_clasificados" + "\\"
                     + "malos_limpios"))]
    pre_processes_conflicts_docs_class = [1 for article in pre_processes_docs]
    pre_processes_docs = pre_processes_docs + pre_processes_conflicts_docs
    pre_processes_docs_class = pre_processes_docs_class + pre_processes_conflicts_docs_class
    return pre_processes_docs, pre_processes_docs_class


def train_classifier():
    pre_processes_docs, pre_processes_docs_class = upload_files_to_train()
    count_vectorizer = CountVectorizer(encoding='utf-8', max_df=1.0, min_df=1, max_features=None,
                                       binary=False).fit(pre_processes_docs)
    pre_processes_docs_vectors = count_vectorizer.transform(pre_processes_docs)
    clf = LogisticRegression()
    clf.fit(pre_processes_docs_vectors.toarray(), pre_processes_docs_class)
    print("clasificador entrenado")
    return clf, count_vectorizer


def classifier_articles(clf, count_vectorizer):
    new_pre_processes_docs = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "cleaned_articles"))]
    new_pre_processes_docs_vectors = count_vectorizer.transform(new_pre_processes_docs)
    new_pre_processes_docs_predicted_class = clf.predict(new_pre_processes_docs_vectors)
    article_classification = [(new_pre_processes_docs[i], new_pre_processes_docs_predicted_class[i]) for i in
                              range(0, len(new_pre_processes_docs))]
    for article in article_classification:
        save_classification_db(article[0], article[1])
    # return [save_classification_db(article[0], article[1]) for article in article_classification]


def save_classification_db(filename, classification):
    try:
        source_path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", filename)
        if classification.astype(int) == 1:
            print(PurePosixPath(source_path), classification)
            update = {
                           "model_classification": True}
            db.update(update, source_path)
            print('update classification on DB')
    except:
        print("no guardo")
        pass


def extract_date(path):
    date_pattern = re.compile(r"^(?P<date>\d{8})")
    regex_match = date_pattern.search(path.replace(' ', ''))
    article_date = datetime.strptime(regex_match.group('date'), '%Y%m%d')
    return article_date.date()
