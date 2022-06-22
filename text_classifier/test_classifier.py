from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import pickle
from joblib import dump, load
import os

pre_processes_docs = [article for article in os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") +
                                                                     "articulos_pre_clasificados" + "\\" +
                                                                     "buenos_limpios"))]
pre_processes_docs_class = [0 for article in pre_processes_docs]

pre_processes_conflicts_docs = [article for article in os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articulos_pre_clasificados" + "\\"
                                                                               + "malos_limpios"))]
pre_processes_conflicts_docs_class = [1 for article in pre_processes_docs]

pre_processes_docs = pre_processes_docs + pre_processes_conflicts_docs
pre_processes_docs_class = pre_processes_docs_class + pre_processes_conflicts_docs_class

conflict_words = ["caso","denuncia","huelga","emergencia","delitos","conflicto","crisis",
"sufrir","difícil","presidio","violaciones","rechazó","auditorías","bloqueo","vulnerando",
"ilegales","advierten","injusticias","crítica","traición","convocó","incumplimiento",
"declarar" ,"reportó","crímenes","destrucción","paro","detención","paralización","alertó",
"movilizaciones","protesta","fraude","violencia","amenaza","agresiones","robar","enfrentar",
"riesgo","caída","proceso","contrabando","afectar","dañar","gasto","multas","problemas"]


save_words = ["garantizó","legales","iniciativa","afluencia","superar","reconocimiento",
"compromiso","gracias","dialogar","apoyo","agradeció","voluntarios","esfuerzo","brigadas","convenio",
"cuidados","desinteresado","responsable","inauguración","bonos","impulsar","destacado","preservar",
"gratuitas","capacitó","derecho","reforzar","campaña","ayudarán","conmemora","operativos",
"feliz","priorizar","recaudaciones","contribuciones","mejora","estima","celebró","satisfacer",
"tecnología","cumplir","desarrollo","homenaje","seguridad","beneficio","participación","aprendió"]


def count_words(article):
    cant = 0
    for word in article.split(' '):
        if word in conflict_words:
            cant = cant + 1
        if word in save_words:
            cant = cant - 1
    return cant

def get_flags():
    flags = []
    for article in pre_processes_docs:
        flags.append(count_words(article))
    return flags



count_vectorizer = CountVectorizer(encoding='utf-8', min_df=0.1, max_features=634).fit(pre_processes_docs, get_flags())

pre_processes_docs_vectors = count_vectorizer.transform(pre_processes_docs)
print(pre_processes_docs_vectors.shape)

clf = LogisticRegression()
clf.fit(pre_processes_docs_vectors.toarray(), pre_processes_docs_class)


new_pre_processes_docs = [article for article in os.listdir(
    os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "test_articles" + "\\" + "buenos"))]
new_pre_processes_docs = new_pre_processes_docs + [article for article in os.listdir(
    os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "test_articles" + "\\" + "malos"))]

new_pre_processes_docs_vectors = count_vectorizer.transform(new_pre_processes_docs)

new_pre_processes_docs_predicted_class = clf.predict(new_pre_processes_docs_vectors)

expected = list(0 for elem in range(0, 35)) + list(1 for elem in range(0, 35))
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

# dump(count_vectorizer, 'classifiers/count_vectorizer.joblib')
# count_vectorizer_loaded = load('classifiers/count_vectorizer.joblib')
# pickle.dump(count_vectorizer, open("classifiers/count_vectorizer.pickle.dat", "wb"))
# loaded_model = pickle.load(open("classifiers/count_vectorizer.pickle.dat", "rb"))
# loaded_count_vectors = loaded_model.transform(pre_processes_docs)


data = [article for article in os.listdir(
    os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "cleaned_articles"))]

new_vecs = count_vectorizer.transform(data)
new_doc_class = clf.predict(new_vecs)

article_classification = [(data[i], new_doc_class[i]) for i in
                              range(0, len(data))]
for article in article_classification:
     print(article[0], article[1])