from datetime import datetime
import os
import re
import string
import os
import requests
from bs4 import BeautifulSoup

LosTiempos = "https://www.lostiempos.com/"
Opinion = "https://www.opinion.com.bo/blog/section/cochabamba"
LaRazon = "https://www.la-razon.com/sociedad/"

def execute():
    __download(LosTiempos)
#     print("text extraction to LosTiempos".format(os.getenv('TEXT_CLASSIFIER_DATA')));
    __download(Opinion)
#     print("text extraction to Opinion".format(os.getenv('TEXT_CLASSIFIER_DATA')));
    __download(LaRazon)
#     print("text extraction to LaRazon".format(os.getenv('TEXT_CLASSIFIER_DATA')));

def __get_divs_LosTiempos(page):
    articles_divs1 = page.body.find_all(name="div", attrs={"class": "views-field-title"})
    articles_divs2 = page.body.find_all(name="div", attrs={"class": "views-field-title term"})
    articles_divs = articles_divs1 + articles_divs2
    return articles_divs

def __get_divs_Opinion (page):
    articles_divs = page.body.find_all(name="h2", attrs={"class": "title title-article"})
    return articles_divs

def __get_divs_la_razon(page):
    articles_divs = page.body.find_all(name="a", attrs={"class": "title"})
    return articles_divs

def __div_links(articles_divs):
    div_links = []
    for article in articles_divs:
        div_links.append(article.find("a"))
    return div_links

def __get_links (articles_divs):
    links = []
    for div_link in __div_links(articles_divs):
        link = div_link.get("href")
        links.append(link)
    return links

def __get_links_la_razon (articles_divs):
    links = []
    for article in articles_divs:
        link = article.get("href")
        links.append(link)
    return links

def __get_fileName_LosTiempos (date_div, title_article):
    article_date=[ date.text for date in date_div]
    match = re.search(r'\d{2}/\d{2}/\d{4}', article_date[0])
    date = datetime.strptime(match.group(), '%d/%m/%Y')
    dateStr = date.strftime("%d %b %Y ")
    article_title = (dateStr +title_article)
    article_title= __remove_punctuation(article_title)
    return article_title

def __get_fileName_Opinion (date_div, title_article):
    article_date=[ date.text for date in date_div]
    article_title = (article_date[0] + title_article)
    article_title= __remove_punctuation(article_title)
    return article_title

def __get_fileName_LaRazon (date_div, title_article):
    match = re.search(r'\d{4}/\d{2}/\d{2}', date_div)
    date = datetime.strptime(match.group(), '%Y/%m/%d')
    dateStr = date.strftime("%d %b %Y ")
    article_title = (dateStr +title_article)
    article_title= __remove_punctuation(article_title)
    return article_title

def __remove_punctuation ( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

def __download_article(title, article):
    path= r'TEXT_CLASSIFIER_DATA'+title
    f= open(path, "a+")
    for paragraph in article:
        f.write(paragraph + "\n")
    f.close()

def __get_articles_LosTiempos(links):
    for link in links:
        response = requests.get("https://www.lostiempos.com"+link)
        page = BeautifulSoup(response.text, "html.parser")
        article_div = page.body.find_all(name="p", attrs={"class": "rtejustify"})
        date_div = page.body.find_all(name="div", attrs={"class": "date-publish"})
        if len(date_div) > 0:
            title_article = page.title.text
            file_name = __get_fileName_LosTiempos(date_div, title_article) + ".txt"
            article_text = [article.get_text().strip() for article in article_div]
            __download_article(file_name, article_text)
        else:
            pass
    print("Done")

def __get_articles_Opinion(links):
    for link in links:
        response = requests.get("https://www.opinion.com.bo"+link)
        page = BeautifulSoup(response.text, "html.parser")
        date_div = page.body.find_all(name="span", attrs={"class": "content-time"})
        article_div = page.body.find_all(name="p", attrs={})
        title_article = page.title.text
        file_name = __get_fileName_Opinion(date_div, title_article) + ".txt"
        article_text = [article.get_text().strip() for article in article_div]
        __download_article(file_name, article_text)
    print("Done")

def __get_articles_LaRazon(links):
    for link in links:
        response = requests.get(link)
        page = BeautifulSoup(response.text, "html.parser")
        article_div = page.body.find_all(name="div", attrs={"class": "article-body"})
        article_text = [article.get_text().strip() for article in article_div]
        title_article = page.title.text
        file_name = __get_fileName_LaRazon(links[0], title_article) + ".txt"
        __download_article(file_name, article_text)
    print("Done")

def __extract_LosTiempos(page):
    articles_divs = __get_divs_LosTiempos(page)
    links = __get_links(articles_divs)
    __get_articles_LosTiempos(links)

def __extract_Opinion(page):
    articles_divs = __get_divs_Opinion(page)
    links = __get_links(articles_divs)
    __get_articles_Opinion(links)

def __extract_LaRazon(page):
    articles_divs = __get_divs_la_razon(page)
    links = __get_links_la_razon(articles_divs)
    __get_articles_LaRazon(links)


def __download(periodico):
    response = requests.get(periodico)
    page = BeautifulSoup(response.text, "html.parser")
    if periodico == "https://www.lostiempos.com/":
        __extract_LosTiempos(page)
    elif periodico == "https://www.opinion.com.bo/blog/section/cochabamba":
        __extract_Opinion(page)
    elif periodico == "https://www.la-razon.com/sociedad/":
        __extract_LaRazon(page)
