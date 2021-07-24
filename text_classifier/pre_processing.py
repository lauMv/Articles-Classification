import os
import re
import spacy
from repository import db

nlp = spacy.load('es_core_news_md')


def execute():
    print("pre processing...")
    clean_articles()


def extract_date(path):
    extraction_date = None
    los_tiempos_pattern = re.compile(r"^/actualidad/(cochabamba|ais)/(?P<date>\d{8})")
    opinion_pattern = re.compile(r"^/articulo/(cochabamba|pais)/.*?/(?P<date>\d{8})")
    la_razon_pattern = re.compile(r"^https://www\.la-razon\.com/nacional/(?P<date>\d{4}/\d{2}/\d{2})")
    regex_match = los_tiempos_pattern.search(path)
    extraction_date = regex_match.group('date')
    if extraction_date is None:
        regex_match = opinion_pattern.search(path)
        extraction_date = regex_match.group('date')
    if extraction_date is None:
        regex_match = la_razon_pattern.search(path)
        extraction_date = regex_match.group('date')
    return extraction_date


def save_on_db(source_file_path, pre_processed_file_path, extraction_date, user_classification, model_classification):
    db.create(source_file_path, pre_processed_file_path, extract_date(source_file_path), None, None)


def clean_articles():
    files = os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articles"))
    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", "")
    print(path)
    for file in files:
        with open(path + file, "r", encoding="utf-8", errors="ignore") as article_file:
            article = article_file.read()
            cleaned = clean_text(article.replace("\n", ""))
            save_cleaned_article(file, cleaned, path)
    print("Clean all articles")


def clean_text(text):
    cleaned_text = []
    with nlp.disable_pipes('tok2vec', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'):
        article_text = list(nlp(text))
        [cleaned_text.append(token.lower_) for token in article_text if (not token.is_punct and not token.is_quote
         and not token.is_space and not token.like_num and not token.is_stop and not token.is_digit
                                                                         and not token.is_oov)]
    return cleaned_text


def save_cleaned_article(name, clean_article, path):
    name_ = "cleaned " + name
    path_ = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "cleaned_articles", name_)
    save_on_db(path, path_,)
    if not os.path.exists(path_):
        print("Guardando artículo limpio en {}".format(path_))
        with open(path_, "a+", encoding="utf-8") as file:
            text = " ".join(clean_article)
            file.write(text)
            file.close()
