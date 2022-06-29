import os
import re
from datetime import datetime
import spacy
from repository import article_db

nlp = spacy.load('es_core_news_md')


def execute():
    print("pre processing...")
    clean_articles()


def extract_date(path):
    date_pattern = re.compile(r"^(?P<date>\d{8})")
    regex_match = date_pattern.search(path.replace(' ', ''))
    article_date = datetime.strptime(regex_match.group('date'), '%Y%m%d')
    return article_date.date()


def add_clean_article_to_db(filename, content):
    try:
        source_path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", filename)
        pre_processed_file_path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "cleaned_articles", filename)
        article = {
                      "source_file_path": source_path,
                      "pre_processed_file_path": pre_processed_file_path,
                      "filename": filename,
                      "extraction_date": extract_date(filename),
                      "paper": "",
                      "article_content": content,
                      "user_classification": "",
                      "model_classification": False,
                      "used_in_classifier": False
                        }
        article_db.create(article)
    except: pass


def clean_articles():
    files = os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles"))
    for file in files:
        path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "cleaned_articles", file)
        if not os.path.exists(path):
            article_path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", file)
            with open(article_path, "r", encoding="utf-8", errors="ignore") as article_file:
                article = article_file.read()
                cleaned = clean_text(article.replace("\n", ""))
                save_cleaned_article(file, cleaned)
                add_clean_article_to_db(file, article)
                print("saved to db:", file)
    print("Clean all articles")


def clean_text(text):
    cleaned_text = []
    with nlp.disable_pipes('tok2vec', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'):
        article_text = list(nlp(text))
        [cleaned_text.append(token.lower_) for token in article_text if (not token.is_punct and not token.is_quote
         and not token.is_space and not token.like_num and not token.is_stop and not token.is_digit
                                                                         and not token.is_oov)]
    return cleaned_text


def save_cleaned_article(filename, clean_article):
    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "cleaned_articles", filename)
    if not os.path.exists(path):
        with open(path, "a+", encoding="utf-8") as file:
            text = " ".join(clean_article)
            file.write(text)
            file.close()
        print("Guardando artículo limpio en {}".format(path))
