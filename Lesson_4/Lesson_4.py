# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath.
# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

from lxml import html
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


def parse_mail_ru():
    response = requests.get('https://news.mail.ru/', headers=header)
    root = html.fromstring(response.text)
    news = root.xpath(
        '//div[contains(@class, "cols__column cols__column_small_percent-50 cols__column_medium_percent-50 cols__column_large_percent-50 link-hdr")]')
    news_list = []
    for news_block in news:
        news_data = {}
        source = news_block.xpath('.//span[contains(@class, "newsitem__param")]')[1].text
        news_name = news_block.xpath('.//span[contains(@class, "newsitem__title-inner")]')[0].text
        link = news_block.xpath('.//a[contains(@class, "newsitem__title link-holder")]/@href')
        date = news_block.xpath('.//span[contains(@class, "newsitem__param js-ago")]/@datetime')
        news_data['source'] = source
        news_data['news_name'] = news_name
        news_data['link'] = link
        news_data['date'] = date
        news_list.append(news_data)

    print(news_list)


parse_mail_ru()


def parse_lenta_ru():
    response = requests.get('https://lenta.ru/', headers=header)
    root = html.fromstring(response.text)
    news_article = root.xpath(
        '//div[contains(@class, "item article")]')
    news_item = root.xpath(
        '//div[contains(@class, "item news b-tabloid__topic_news")]')
    all_news = []
    all_news.extend(news_article)
    all_news.extend(news_item)
    news_list = []
    for news_block_article in all_news:
        news_data = {}
        link = news_block_article.xpath('.//a[contains(@class, "titles")]/@href')[0]
        article_response = requests.get('https://lenta.ru' + link, headers=header)
        root_article = html.fromstring(article_response.text)
        source = root_article.xpath('//span[contains(@class, "name")]')
        if len(source) > 0:
            source = source[0].text
        else:
            source = None
        news_name = news_block_article.xpath('.//h3[contains(@class, "card-title")]')[0].text
        date = root_article.xpath('.//time[contains(@class, "g-date")]/@datetime')
        news_data['source'] = source
        news_data['news_name'] = news_name
        news_data['link'] = link
        news_data['date'] = date
        news_list.append(news_data)

    print(news_list)


parse_lenta_ru()
