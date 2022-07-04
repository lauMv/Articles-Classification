import os
import pickle
from datetime import datetime

from repository import classifier_db
from .classifier import Classifier
from .model import train_model


path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "cleaned_articles")


def get_date_title(filename):
    date = filename.split()[0]
    return date


def execute():
    print("entrenando clasificador...")
    train_docs, train_docs_class, test_docs, test_docs_class = upload_files_to_set()
    train_model(False, train_docs, train_docs_class,test_docs, test_docs_class)
    print("cargando el modelo")
    loaded_model = load_classifier()
    loaded_model.show_metricts()
    today = datetime.today().strftime('%Y%m%d')
    today_str = str(today).replace(" ", "")
    data = [article for article in os.listdir(path) if get_date_title(article) == today_str]
    print("cant de articulos", len(data))
    predicted = loaded_model.predict(data)
    loaded_model.save_model_classification(predicted, data)
    print(len(predicted))


def load_classifier():
    version = classifier_db.get_use_classifier()
    classifier_name = './text_classifier/classifiers/model_{0}.pkl'.format(version)
    loaded_model = pickle.load(open(classifier_name, "rb"))
    return loaded_model


def get_articles(folder, folder_type):
    articles = []
    files = os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), folder, folder_type))
    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), folder, folder_type, "")
    for file in files:
        with open(path + file, "r", encoding="utf-8", errors="ignore") as article_file:
            articles.append(article_file.read())
    return articles


def upload_files_to_set():
    pre_processes_docs = get_articles("articulos_pre_clasificados", "buenos_limpios")
    pre_processes_docs_conflicts = get_articles("articulos_pre_clasificados", "malos_limpios")
    pre_processes_docs_class = [0 for elen in range(0, len(pre_processes_docs))] + \
                               [1 for elem in range(0, len(pre_processes_docs_conflicts))]
    pre_processes_docs = pre_processes_docs + pre_processes_docs_conflicts

    new_pre_processes_docs = get_articles("test_articles", "buenos")
    new_pre_processes_docs_conflicts = get_articles("test_articles", "malos")
    new_pre_processes_docs_predicted_class = [0 for elem in range(0, len(new_pre_processes_docs))] + \
                                             [1 for elem in range(0, len(new_pre_processes_docs_conflicts))]
    new_pre_processes_docs = new_pre_processes_docs + new_pre_processes_docs_conflicts
    return pre_processes_docs, pre_processes_docs_class, new_pre_processes_docs, new_pre_processes_docs_predicted_class

