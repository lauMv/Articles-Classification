import os
import re
from datetime import datetime

import spacy
from repository import db

nlp = spacy.load('es_core_news_md')


def execute():
    print("pre processing...")
    clean_articles()


def extract_date(path):
    opinion_pattern = re.compile(r"^(?P<date>\d{8})")
    regex_match = opinion_pattern.search(path)
    article_date = datetime.strptime(regex_match.group('date'), '%Y%m%d')
    return article_date.date()


def add_clean_article_to_db(path, pre_processed_file_path, name):
    source_path = path + " " + name
    article = {
                  "source_file_path": source_path,
                  "pre_processed_file_path": pre_processed_file_path,
                  "extraction_date": extract_date(name),
                  "user_classification": None,
                  "model_classification": None}
    db.create(article)


def clean_articles():
    files = os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articles"))
    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", "")
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
    if not os.path.exists(path_):
        print("Guardando artículo limpio en {}".format(path_))
        add_clean_article_to_db(path, path_, name)
        with open(path_, "a+", encoding="utf-8") as file:
            text = " ".join(clean_article)
            file.write(text)
            file.close()
