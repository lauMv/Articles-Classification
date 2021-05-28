import os
import re
import string
from datetime import datetime

import requests
from bs4 import BeautifulSoup

LOS_TIEMPOS_BASE_URL = "https://www.lostiempos.com/actualidad/cochabamba"
OPINION_BASE_URL = "https://www.opinion.com.bo/blog/section/cochabamba"
LA_RAZON_BASE_URL = "https://www.la-razon.com/nacional/"


def execute():
    print("Iniciando el proceso de extracción en {}".format(os.getenv("TEXT_CLASSIFIER_DATA")))
    __extract_text(LOS_TIEMPOS_BASE_URL)
    __extract_text(OPINION_BASE_URL)
    __extract_text(LA_RAZON_BASE_URL)


def __div_links(articles_divs):
    div_links = []
    for article in articles_divs:
        div_links.append(article.find("a"))
    return div_links


def __get_links(articles_divs):
    links = []
    for div_link in __div_links(articles_divs):
        link = div_link.get("href")
        links.append(link)
    return links


def __remove_punctuation(text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)


def __download_article(title, article):
    path = os.getenv("TEXT_CLASSIFIER_DATA") + "articles\\" + title
    print("Guardando artículo en {}".format(path))
    article_file = open(path, "a+")
    for paragraph in article:
        if paragraph is not None:
            article_file.write(paragraph + "\n")
        else:
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

    def __get_articles_los_tiempos(articles_links):
        for link in articles_links:
            response = requests.get("https://www.lostiempos.com" + link)
            article_page = BeautifulSoup(response.text, "html.parser")
            article_div = article_page.body.find_all(name="p", attrs={"class": "rtejustify"})
            date_div = article_page.body.find_all(name="div", attrs={"class": "date-publish"})
            if len(date_div) > 0:
                title_article = article_page.title.text
                file_name = __get_file_name_los_tiempos(date_div, title_article) + ".txt"
                article_text = [article.get_text().strip() for article in article_div]
                if os.path.exists(file_name):
                    pass
                else:
                    __download_article(file_name, article_text)
            else:
                pass
        print("Done")

    articles_divs = __get_divs_los_tiempos(page)
    links = __get_links(articles_divs)
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

    def __get_articles_opinion(articles_links):
        for link in articles_links:
            response = requests.get("https://www.opinion.com.bo" + link)
            article_page = BeautifulSoup(response.text, "html.parser")
            date_div = article_page.body.find_all(name="span", attrs={"class": "content-time"})
            article_div = article_page.body.find_all(name="p", attrs={})
            title_article = article_page.title.text
            file_name = __get_file_name_opinion(date_div, title_article) + ".txt"
            article_text = [article.get_text().strip() for article in article_div]
            __download_article(file_name, article_text)
        print("Done")

    articles_divs = __get_divs_opinion(page)
    links = __get_links(articles_divs)
    __get_articles_opinion(links)


def __extract_la_razon(page):

    def __get_divs_la_razon(page_div):
        article_divs = page_div.body.find_all(name="a", attrs={"class": "title"})
        return article_divs

    def __get_links_la_razon(article_divs):
        articles_links = []
        for article in article_divs:
            link = article.get("href")
            articles_links.append(link)
        return articles_links

    def __get_file_name_la_razon(date_div, title_article):
        match = re.search(r'\d{4}/\d{2}/\d{2}', date_div)
        date = datetime.strptime(match.group(), '%Y/%m/%d')
        date_str = date.strftime("%d %b %Y ")
        article_title = (date_str + title_article)
        article_title = __remove_punctuation(article_title)
        return article_title

    def __get_articles_la_razon(articles_links):
        for link in articles_links:
            response = requests.get(link)
            article_page = BeautifulSoup(response.text, "html.parser")
            article_div = article_page.body.find_all(name="div", attrs={"class": "article-body"})
            article_text = [article.get_text().strip() for article in article_div]
            title_article = article_page.title.text
            file_name = __get_file_name_la_razon(link, title_article) + ".txt"
            __download_article(file_name, article_text)
        print("Done")

    articles_divs = __get_divs_la_razon(page)
    links = __get_links_la_razon(articles_divs)
    __get_articles_la_razon(links)


def __extract_text(base_url):
    response = requests.get(base_url)
    page = BeautifulSoup(response.text, "html.parser")
    if base_url == "https://www.lostiempos.com/":
        __extract_los_tiempos(page)
    elif base_url == "https://www.opinion.com.bo/blog/section/cochabamba":
        __extract_opinion(page)
    elif base_url == "https://www.la-razon.com/nacional/":
        __extract_la_razon(page)
