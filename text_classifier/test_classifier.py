from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

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

count_vectorizer = CountVectorizer(encoding='utf-8', max_df=1.0, min_df=1, max_features=None,
                                   binary=False).fit(pre_processes_docs)

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

expected = list(0 for elem in range(0, 35)) + list(1 for elem in range(0,35))
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
