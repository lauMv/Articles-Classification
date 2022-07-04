import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import pickle
from joblib import dump, load
import os
from datetime import datetime



#articulos de entrenamiento
from repository import article_db


def set_data():
    pre_processes_docs = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articulos_pre_clasificados" + "\\" + "buenos_limpios"))]
    pre_processes_conflicts_docs = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articulos_pre_clasificados" + "\\" + "malos_limpios"))]

    clasificacion_doc_procesados = [0 for article in range(0, len(pre_processes_docs))] + [1 for article in
                                                                            range(0, len(pre_processes_conflicts_docs))]
    lista_documeentos_procesados = pre_processes_docs + pre_processes_conflicts_docs

    new_pre_processes_docs = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "test_articles" + "\\" + "buenos"))]
    new_pre_processes_conflicts_docs = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "test_articles" + "\\" + "malos"))]

    expected = [0 for elem in range(0, len(new_pre_processes_docs))] + [1 for elem in
                                                                        range(0, len(new_pre_processes_conflicts_docs))]
    new_pre_processes_docs = new_pre_processes_docs + new_pre_processes_conflicts_docs
    return lista_documeentos_procesados, clasificacion_doc_procesados, new_pre_processes_docs, expected



def execute_():
    lista_documentos_procesados, clasificacion_doc_procesados, new_pre_processes_docs, expected = set_data()
    train(lista_documentos_procesados, clasificacion_doc_procesados, new_pre_processes_docs, expected)


conflict_words = ["caso", "denuncia", "huelga", "emergencia", "delitos", "conflicto", "crisis",
                      "sufrir", "difícil", "presidio", "violaciones", "rechazó", "auditorías", "bloqueo", "vulnerando",
                      "ilegales", "advierten", "injusticias", "crítica", "traición", "convocó", "incumplimiento",
                      "declarar", "reportó", "crímenes", "destrucción", "paro", "detención", "paralización", "alertó",
                      "movilizaciones", "protesta", "fraude", "violencia", "amenaza", "agresiones", "robar",
                      "enfrentar",
                      "riesgo", "caída", "proceso", "contrabando", "afectar", "dañar", "gasto", "multas", "problemas"]

save_words = ["garantizó", "legales", "iniciativa", "afluencia", "superar", "reconocimiento",
                  "compromiso", "gracias", "dialogar", "apoyo", "agradeció", "voluntarios", "esfuerzo", "brigadas",
                  "convenio",
                  "cuidados", "desinteresado", "responsable", "inauguración", "bonos", "impulsar", "destacado",
                  "preservar",
                  "gratuitas", "capacitó", "derecho", "reforzar", "campaña", "ayudarán", "conmemora", "operativos",
                  "feliz", "priorizar", "recaudaciones", "contribuciones", "mejora", "estima", "celebró", "satisfacer",
                  "tecnología", "cumplir", "desarrollo", "homenaje", "seguridad", "beneficio", "participación",
                  "aprendió"]


def count_words(article):
    cant = 0
    for word in article.split(' '):
        if word in conflict_words:
            cant = cant + 1
        if word in save_words:
            cant = cant - 1
    return cant


def get_flags(pre_processes_docs):
    flags = []
    for article in pre_processes_docs:
        flags.append(count_words(article))
    return flags


def save_classification_in_db(article_classification):
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

    for article in article_classification:
        print(article[0], article[1])
        save_classification_db(article[0], article[1])
    pass





#iniciar la matriz con documentos originales
def train(lista_documeentos_procesados, clasificacion_doc_procesados, new_pre_processes_docs,expected):
    count_vectorizer = CountVectorizer(encoding='utf-8', min_df=0.1, max_features=634).\
        fit(lista_documeentos_procesados)

#transforma en vectores los documentos
    pre_processes_docs_vectors = count_vectorizer.transform(lista_documeentos_procesados)
    print(pre_processes_docs_vectors.shape)

#inicia el calsificador#
    clf = LogisticRegression()
    clf.fit(pre_processes_docs_vectors.toarray(), clasificacion_doc_procesados)


#articulos de prueba

#transorma los documentos de prueba en vectores
    new_pre_processes_docs_vectors = count_vectorizer.transform(new_pre_processes_docs)

#predice
    new_pre_processes_docs_predicted_class = clf.predict(new_pre_processes_docs_vectors)

#
#Evaluacion
# accuracy
    print('accuracy {0:.2f}'.format(accuracy_score(expected, clf.predict(new_pre_processes_docs_vectors))))
    # confusion matrix
    print('matriz de confusión \n {0}'.format(confusion_matrix(expected, clf.predict(new_pre_processes_docs_vectors))))
    # precision
    print('precision {0:.2f}'.format(precision_score(expected, clf.predict(new_pre_processes_docs_vectors))))
    # recall
    print('recall {0:.2f}'.format(recall_score(expected, clf.predict(new_pre_processes_docs_vectors))))
    # f1
    print('f1 {0:.2f}'.format(f1_score(expected, clf.predict(new_pre_processes_docs_vectors))))


    print('Clasificando los Documentos descargados:')

    def get_date_title(filename):
        date = filename.split()[0]
        return date

    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "cleaned_articles")

    today = datetime.today().strftime('%Y%m%d')
    today_str = str(today).replace(" ", "")
    # for article in os.listdir(path):
    #     if get_date_title(article) == today_str:
    #         data.append(article)
    data = [article for article in os.listdir(path) if get_date_title(article) == today_str]
    new_vecs = count_vectorizer.transform(data)
    new_doc_class = clf.predict(new_vecs)

    article_classification = [(data[i], new_doc_class[i]) for i in range(0, len(data))]
    save_classification_in_db(article_classification)



