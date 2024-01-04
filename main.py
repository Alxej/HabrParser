from news_parser import HabrParser
import io
if __name__ == "__main__":
    a = HabrParser()
    print(a.articles)
    with io.open("article.txt", encoding="utf-8", mode="w") as jok:
        jok.write(str(a.articles[1]))