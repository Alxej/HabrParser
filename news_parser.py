from bs4 import BeautifulSoup
from accessify import private
import requests


class HabrParser():
    limit = 10
    articles = []

    def __init__(self, articles_limit: int = 10):
        self.limit = articles_limit
        self.load_last_articles_dictionary()
    
    @private
    def load_last_articles_dictionary(self):
        urls = self.get_last_article_urls(self.limit)
        for url in urls:
            try:
                doc = self.download_document(url)
                if doc['status'] == 'ok':
                    self.articles.append(doc)
            except Exception:
                continue

    @private
    def get_last_article_urls(self, n: int):
        # получаем rss ленту новостей длины n
        url = requests.get(f"https://habr.com/ru/rss/articles/?limit={n}.?with_hubs=true")
        # если запрос возвращает ошибку, то выкидываем ошибку
        if not url.ok:
            raise Exception("rss is not loaded")
        
        # получаем ссылки на статьи
        soup = BeautifulSoup(url.content, "xml")
        items = soup.find_all('item')
        links = [item.link.text for item in items]

        return links

    def download_document(self, url):
        # выгрузка документа
        r = requests.get(url)
        # парсинг документа
        soup = BeautifulSoup(r.text, 'html5lib') # instead of html.parser
        doc = {}
        doc['link'] = url
        
        if not soup.find("h1", {"class": "tm-title tm-title_h1"}):
            # такое бывает, если статья не существовала или удалена
            doc['status'] = 'title_not_found'
        else:
            
            doc['status'] = 'ok'
            doc['title'] = soup.find("h1", {"class": "tm-title tm-title_h1"}).text
            ps = soup.find_all("p")
            doc['text'] = ""
            # собираем весь текст статьи
            for p in ps:
                text = p.text.replace('\xa0', " ").replace('\xad', " ")
                doc['text'] += text
            # собираем все подзаголовки
            doc['subtitles'] = []
            for i in range(2, 6):
                hs = soup.find_all(f"h{i}")
                for h in hs:
                    text = h.text.replace('\xa0', "")
                    doc['subtitles'].append(text)
            # теги
            tags = soup.find_all("a", {"class": "tm-tags-list__link"})
            doc['tags'] = [tag.text for tag in tags]
            # хабы
            hubs = soup.find_all("a", {"class": "tm-hubs-list__link"})
            doc['hubs'] = [hub.text for hub in hubs]
        return doc