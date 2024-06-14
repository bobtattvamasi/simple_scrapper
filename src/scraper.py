import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
import psycopg2
import pandas as pd

import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger('simple_scrapper')
logger.setLevel(logging.INFO)

class NewsArticle(BaseModel):
    title: str
    text: str
    date: str
    url: str

class NewsArticleList:
    def __init__(self):
        self.articles = []

    def add_article(self, news_article):
        self.articles.append(news_article)

    def save_to_csv(self):
        header = ['title', 'text', 'date', 'url']
        df = pd.DataFrame(self.articles, columns=header)
        df.to_csv("./kinopoisk_news_data.csv", sep=';', encoding='utf8')


def scrape_website(url):
    logger.info('scraping website starting')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    logger.info('get request from site url: %s' % url)
    #logger.info(f"response status code: {soup}")

    # Извлечение данных с помощью XPath или CSS-селекторов
    articles = soup.findAll('div', class_='posts-grid__main-section-column')  # Пример использования CSS-селектора

    news_article_list = NewsArticleList()

    #logger.info(f"getting articles from page. articles: {articles}")

    for article in articles:
        anchor_tag = article.find('a')  # Find the anchor tag
        title = article.find('h3').text
        # ... (rest of your code to get text and date)

        url = anchor_tag['href']
        aria_label = anchor_tag.get('aria-label')  # Use get method for optional attribute

        news_article = NewsArticle(title=title, text=aria_label, date='today', url=url)

        print(f" New Article is: {news_article}")

        news_article_list.add_article(news_article)

    news_article_list.save_to_csv()

        # Обработка и валидация данных с помощью Pydantic
        # ...

        # Сохранение данных в базу данных
        #save_to_database(news_article)

def save_to_database(news_article):
    connection = psycopg2.connect(dbname='your_database', user='your_user', password='your_password', host='your_host')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO news_articles (title, text, date, url) VALUES (%s, %s, %s, %s)',
                   (news_article.title, news_article.text, news_article.date, news_article.url))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    logger.info('Starting')
    url = 'https://www.kinopoisk.ru/media/news/'  # Пример URL веб-сайта
    scrape_website(url)
