import os
import spacy

nlp = spacy.load('es_core_news_md')
files = os.listdir(os.getenv("TEXT_CLASSIFIER_DATA"))


def execute():
    print("pre processing...")
    clean_articles()


def clean_articles():
    path = os.getenv("TEXT_CLASSIFIER_DATA")
    for file in files:
        article_file = open(path + file, "r")
        article = str(article_file.read())
        cleaned = clean_text(article)
        save_cleaned_article(file, cleaned)
    print("Clean all articles")


def clean_text(text):
    cleaned_text = []
    with nlp.disable_pipes('tok2vec', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'):
        article_text = list(nlp(text))
        [cleaned_text.append(str(token)) for token in article_text if not token.is_stop and not token.is_punct and not token.is_digit]
    return cleaned_text


def save_cleaned_article(name, clean_article):
    path_ = os.getenv("TEXT_CLASSIFIER_CLEAN_DATA") + "cleaned " + name
    print("Guardando artículo limpio en {}".format(path_))
    file = open(path_, "a+")
    for word in clean_article:
        file.write(word + " ")
    file.close()
    print("Done")
