import os
import spacy

nlp = spacy.load('es_core_news_md')


def execute():
    print("pre processing...")
    clean_articles()


def clean_articles():
    files = os.listdir(os.path.join(os.getenv("TEXT_CLASSIFIER_DATA") + "articles"))
    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", "")
    print(path)
    for file in files:
        with open(path + file, "r", encoding="utf-8", errors="ignore") as article_file:
            article = article_file.read()
            cleaned = clean_text(article.replace("\n", ""))
            save_cleaned_article(file, cleaned)
    print("Clean all articles")


def clean_text(text):
    cleaned_text = []
    with nlp.disable_pipes('tok2vec', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'):
        article_text = list(nlp(text))
        [cleaned_text.append(token.lower_) for token in article_text if (not token.is_punct and not token.is_quote
         and not token.is_space and not token.like_num and not token.is_stop and not token.is_digit
                                                                         and not token.is_oov)]
    return cleaned_text


def save_cleaned_article(name, clean_article):
    name_ = "cleaned " + name
    path_ = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "cleaned_articles", name_)
    if not os.path.exists(path_):
        print("Guardando artículo limpio en {}".format(path_))
        with open(path_, "a+", encoding="utf-8") as file:
            text = " ".join(clean_article)
            file.write(text)
            file.close()
