import newspaper
from bs4 import BeautifulSoup
import urllib.request
import nltk
import numpy as np
from rss_parser import Parser
import requests
class HabrParser():
    url_list = []
    categories = []
    categories_codenames = []

    def __init__(self, russian_categories: list = None):
        self.categories = russian_categories
        self.init_categories_real_name()

    def init_categories_real_name(self):
        codename_dictionary = {
            "Политика": "politics", "Общество": "society",
            "Экономика": "economy", "Армия": "defense_safety", 
            "Безопасность": "defense_safety",
            "В мире": "world", "Туризм": "tourism",
            "Происшествия": "incidents", "Культура": "culture",
            "Технологии": "computers", "Наука": "science",
            "Религия": "religion"
        }

        if self.categories is None:
            self.categories_codenames = codename_dictionary.values()
        else:
            self.categories_codenames = [codename_dictionary[category] for category in self.categories if category in codename_dictionary.keys()]
    

    def download_document(self,pid):
        # выгрузка документа
        r = requests.get('https://habr.com/ru/articles/783641/')
        # парсинг документа
        soup = BeautifulSoup(r.text, 'html5lib') # instead of html.parser
        doc = {}
        doc['id'] = pid
        
        if not soup.find("h1", {"class": "tm-title tm-title_h1"}):
            # такое бывает, если статья не существовала или удалена
            doc['status'] = 'title_not_found'
        else:
            
            doc['status'] = 'ok'
            doc['title'] = soup.find("h1", {"class": "tm-title tm-title_h1"}).text
            print (doc['title'])
            doc['text'] = soup.find("div", {"class": "post__text"}).text
            doc['time'] = soup.find("span", {"class": "post__time"}).text
            


if __name__ == "__main__":
    a = HabrParser()
    for i in range(100000, 101000):
        a.download_document(i)