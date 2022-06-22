# This Python file uses the following encoding: utf-8

from repository import article_db

from text_classifier.model import Model
import os


def execute():
    print("clasificando...")
    model = Model()
    train_model(model)
    data = [article for article in os.listdir(
        os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "cleaned_articles"))]
    predicted = predict_articles(model, data)
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
    pre_processes_docs = pre_processes_docs + get_articles("articulos_pre_clasificados", "malos_limpios")
    pre_processes_docs_class = list(0 for elen in range(0, 35)) + list(1 for elem in range(0, 35))

    new_pre_processes_docs = get_articles("test_articles", "buenos")
    new_pre_processes_docs = new_pre_processes_docs + get_articles("test_articles", "malos")
    new_pre_processes_docs_predicted_class = list(0 for elem in range(0, 35)) + list(1 for elem in range(0, 35))

    return pre_processes_docs, pre_processes_docs_class, new_pre_processes_docs, new_pre_processes_docs_predicted_class


conflict_words = ["caso", "denuncia","huelga","emergencia","delitos","conflicto","crisis",
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


def get_flags(pre_processes_docs):
    flags = []
    for article in pre_processes_docs:
        flags.append(count_words(article))
    return flags


def train_model(model):
    train_docs, train_docs_class, new_docs, new_docs_class = upload_files_to_set()

    model.vectorizer.fit(train_docs, get_flags(train_docs))
    pre_processes_docs_vectors = model.vectorizer.transform(train_docs)
    model.clf.fit(pre_processes_docs_vectors.toarray(), train_docs_class)
    # model.flags = get_flags(train_docs)
    # model.fit(train_docs, train_docs_class)
    # vec = model.fit_transform(train_docs)
    # model.fit(vec.toarray(), train_docs_class)

    new_docs_vec = model.vectorizer.transform(new_docs)
    new_docs_predicted_class = model.clf.predict(new_docs_vec)
    #
    # vec2 = model.fit_transform(new_docs)
    # model.predict(vec2)
    # model.eval_model(new_docs_class, vec2)
    print("clasificador entrenado")


def predict_articles(model, new_docs):
    new_docs = model.fit_transform(new_docs)
    classification = model.predict(new_docs)
    article_classification = [(new_docs[i], classification[i]) for i in range(0,len(new_docs))]
    # new_docs_vectors = model.vectorizer.transform(new_docs)
    # new_docs_predicted_class = model.clf.predict(new_docs_vectors)
    # article_classification = [(new_docs[i], new_docs_predicted_class[i]) for i in
    #                           range(0, len(new_docs))]
    for article in article_classification:
        print(article[0], article[1])
        save_classification_db(article[0], article[1])
    print('classification saved on DB')
    return classification


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

