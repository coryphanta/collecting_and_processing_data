import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from Lesson_5.leroy.leroy.items import LeroySpiderItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['https://leroymerlin.ru/']
    start_urls = ['https://leroymerlin.ru/catalogue/cvetushchie-rasteniya/']

    def parse(self, response):
        item_links = response.css('.p7w1ji8_plp > div > div > a::attr(href)').extract()
        for link in item_links:
            yield response.follow(link, callback=self.parse_items)


    def parse_items(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroySpiderItem(), response=response)

        loader.add_css('title',
                       'span.t9jup0e_plp p1h8lbu4_plp::text')

        loader.add_css('images',
                       'picture[class*="p10zxbd6_plp"]::attr(srcset)')

        loader.add_css('price', 'li.item-params-list-item ::text')

        loader.add_value('url', response.url)

        yield loader.load_item()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(LeroySpider)
process.start()
