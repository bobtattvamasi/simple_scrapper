import requests
from bs4 import BeautifulSoup
import psycopg2
from models import NewsArticle, NewsArticleList
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger('simple_scrapper')
logger.setLevel(logging.INFO)




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
        date = 'today'

        news_article = [title, aria_label, date, url] #NewsArticle(title=title, text=aria_label, date='today', url=url)

        print(f" New Article is: {news_article}")

        news_article_list.add_article(news_article)

    news_article_list.save_to_csv()

        # Обработка и валидация данных с помощью Pydantic
        # ...

        # Сохранение данных в базу данных
        #save_to_database(news_article)

def save_to_database(news_article):
    connection = psycopg2.connect(dbname='FaqMarketing', user='FaqMarketing', password='098', host='localhost')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO news_articles (title, text, date, url) VALUES (%s, %s, %s, %s)',
                   (news_article.title, news_article.text, news_article.date, news_article.url))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    logger.info('Starting')
    url = 'https://www.kinopoisk.ru/media/news/'  # Пример URL веб-сайта
    scrape_website(url)
