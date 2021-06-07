import os
import re
import string
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

LOS_TIEMPOS_BASE_URL = "https://www.lostiempos.com/actualidad/cochabamba"
OPINION_BASE_URL = "https://www.opinion.com.bo/blog/section/cochabamba/"
LA_RAZON_BASE_URL = "https://www.la-razon.com/nacional/"


def execute():
    print("Iniciando el proceso de extracción en {}".format(os.getenv("TEXT_CLASSIFIER_DATA")))
    __extract_text(LOS_TIEMPOS_BASE_URL)
    __extract_text(OPINION_BASE_URL)
    __extract_text(LA_RAZON_BASE_URL)


def __div_links(articles_divs):
    return [article.find("a") for article in articles_divs]


def __get_links(articles_divs, is_valid):
    links = [link.get("href") for link in __div_links(articles_divs)]
    return [link for link in links if is_valid(link)]


def __remove_punctuation(text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)


def __download_article(title, article):
    path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", title)
    print("Guardando artículo en {}".format(path))
    article_file = open(path, "a+")
    for paragraph in article:
        try:
            if paragraph is not None:
                article_file.write(paragraph)
                article_file.write("\n")
        except:
            continue
    article_file.close()


def __extract_los_tiempos(page):

    def __get_divs_los_tiempos(page_div):
        articles_divs1 = page_div.body.find_all(name="div", attrs={"class": "views-field-title"})
        articles_divs2 = page_div.body.find_all(name="div", attrs={"class": "views-field-title term"})
        article_divs = articles_divs1 + articles_divs2
        return article_divs

    def __get_file_name_los_tiempos(date_div, title_article):
        article_date = [date.text for date in date_div]
        match = re.search(r'\d{2}/\d{2}/\d{4}', article_date[0])
        date = datetime.strptime(match.group(), '%d/%m/%Y')
        date_str = date.strftime("%d %b %Y ")
        article_title = (date_str + title_article)
        article_title = __remove_punctuation(article_title)
        return article_title

    def build_validation_function_for_los_tiempos():
        los_tiempos_pattern = re.compile(r"^/actualidad/(cochabamba|pais)/(?P<date>\d{8})")
        los_tiempos_date_str = datetime.today().strftime('%Y%m%d')

        def is_valid_for_los_tiempos(link):
            regex_match = los_tiempos_pattern.search(link)
            return (regex_match is not None) and (regex_match.group('date') == los_tiempos_date_str)

        return is_valid_for_los_tiempos

    def __get_articles_los_tiempos(articles_links):
        for link in articles_links:
            response = requests.get("https://www.lostiempos.com" + link)
            article_page = BeautifulSoup(response.text, "html.parser")
            article_div = article_page.body.find_all(name="p", attrs={"class": "rtejustify"})
            date_div = article_page.body.find_all(name="div", attrs={"class": "date-publish"})
            title_article = article_page.title.text
            file_name = __get_file_name_los_tiempos(date_div, title_article) + ".txt"
            article_text = [article.get_text().strip() for article in article_div]
            if not os.path.exists(file_name):
                __download_article(file_name, article_text)
        print("Done")

    articles_divs = __get_divs_los_tiempos(page)
    links = __get_links(articles_divs, build_validation_function_for_los_tiempos())
    __get_articles_los_tiempos(links)


def __extract_opinion(page):

    def __get_divs_opinion(page_div):
        article_divs = page_div.body.find_all(name="h2", attrs={"class": "title title-article"})
        return article_divs

    def __get_file_name_opinion(date_div, title_article):
        article_date = [date.text for date in date_div]
        article_title = (article_date[0] + title_article)
        article_title = __remove_punctuation(article_title)
        return article_title

    def build_validation_function_for_opinion():
        opinion_pattern = re.compile(r"^/articulo/(cochabamba|pais)/.*?/(?P<date>\d{8})")
        opinion_date_str = datetime.today().strftime('%Y%m%d')

        def is_valid_for_opinion(link):
            regex_match = opinion_pattern.search(link)
            return (regex_match is not None) and (regex_match.group('date') == opinion_date_str)

        return is_valid_for_opinion

    def __get_articles_opinion(articles_links):
        for link in articles_links:
            response = requests.get("https://www.opinion.com.bo" + link)
            article_page = BeautifulSoup(response.text, "html.parser")
            date_div = article_page.body.find_all(name="span", attrs={"class": "content-time"})
            article_div = article_page.body.find_all(name="p", attrs={})
            title_article = article_page.title.text
            file_name = __get_file_name_opinion(date_div, title_article) + ".txt"
            article_text = [article.get_text().strip() for article in article_div]
            if not os.path.exists(file_name):
                __download_article(file_name, article_text)
        print("Done")

    articles_divs = __get_divs_opinion(page)
    links = __get_links(articles_divs, build_validation_function_for_opinion())
    __get_articles_opinion(links)


def __extract_la_razon(page):

    def __get_divs_la_razon(page_div):
        article_divs = page_div.body.find_all(name="a", attrs={"class": "title"})
        return article_divs

    def __get_links_la_razon(article_divs, is_valid):
        article_links = [article.get("href") for article in article_divs]
        return [link for link in article_links if is_valid(link)]

    def __get_file_name_la_razon(date_div, title_article):
        match = re.search(r'\d{4}/\d{2}/\d{2}', date_div)
        date = datetime.strptime(match.group(), '%Y/%m/%d')
        date_str = date.strftime("%d %b %Y ")
        if datetime.now().day == date.day and datetime.now().month == date.month:
            article_title = (date_str + title_article)
            article_title = __remove_punctuation(article_title)
        else:
            article_title = ""
        return article_title

    def build_validation_function_for_la_razon():
        la_razon_pattern = re.compile(r"^https://www\.la-razon\.com/nacional/(?P<date>\d{4}/\d{2}/\d{2})")
        la_razon_date_str = datetime.today().strftime('%Y/%m/%d')

        def is_valid_for_la_razon(link):
            regex_match = la_razon_pattern.search(link)
            return (regex_match is not None) and (regex_match.group('date') == la_razon_date_str)

        return is_valid_for_la_razon

    def __get_articles_la_razon(articles_links):
        for link in articles_links:
            response = requests.get(link)
            article_page = BeautifulSoup(response.text, "html.parser")
            article_div = article_page.body.find_all(name="div", attrs={"class": "article-body"})
            article_text = [article.get_text().strip() for article in article_div]
            title_article = article_page.title.text
            file_name = __get_file_name_la_razon(link, title_article) + ".txt"
            if not os.path.exists(file_name):
                __download_article(file_name, article_text)
        print("Done")

    articles_divs = __get_divs_la_razon(page)
    links = __get_links_la_razon(articles_divs, build_validation_function_for_la_razon())
    __get_articles_la_razon(links)


def __extract_text(base_url):
    response = requests.get(base_url)
    page = BeautifulSoup(response.text, "html.parser")
    if base_url == "https://www.lostiempos.com/actualidad/cochabamba":
        __extract_los_tiempos(page)
    elif base_url == "https://www.opinion.com.bo/blog/section/cochabamba/":
        __extract_opinion(page)
    elif base_url == "https://www.la-razon.com/nacional/":
        __extract_la_razon(page)


if __name__ == "__main__":
    execute()