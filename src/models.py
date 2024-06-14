from pydantic import BaseModel
import pandas as pd

class NewsArticle(BaseModel):
    title: str
    text: str
    date: str
    url: str

class NewsArticleList:
    def __init__(self):
        self.articles = []
        self.save_path = "./data/saved_data"

    def add_article(self, news_article):
        self.articles.append(news_article)

    def save_to_csv(self):
        header = ['title', 'text', 'date', 'url']
        df = pd.DataFrame(self.articles, columns=header)
        df.to_csv(f"{self.save_path}/kinopoisk_news_data.csv", sep=';', encoding='utf8')