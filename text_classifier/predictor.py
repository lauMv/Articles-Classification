import os
from .classifier import Classifier


def execute():
    classifier = Classifier()
    print("clasificando...")
    train_docs, train_docs_class, test_docs, test_docs_class = upload_files_to_set()
    classifier.train_model_local('0', False, train_docs, train_docs_class, test_docs, test_docs_class)
    print("evaluando modelo")
    predicted = classifier.predict(test_docs)
    classifier.evaluate(test_docs_class, predicted)
    classifier.print_eval()
    data = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "cleaned_articles"))]
    classifier.predict(data)
    print(len(predicted))


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

