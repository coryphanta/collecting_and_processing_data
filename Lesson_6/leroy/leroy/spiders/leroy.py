import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from Lesson_5.leroy.leroy.items import LeroySpiderItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/cvetushchie-rasteniya/']
    # start_urls = [
    #     # f'https://www.avito.ru/rossiya/bytovaya_elektronika?q={mark}']
    #     f'https://leroymerlin.ru/catalogue/kraski/']

    def parse(self, response):
        next_page = response.css(
            'a[data-qa-pagination-item="right"]::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        ads_links = response.css(
            '.p7w1ji8_plp > div > div > a::attr(href)').getall()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_items)

        # item_links = response.css('.p7w1ji8_plp > div > div > a::attr(href)').extract()
        # for link in item_links:
        #     txt_response = response.follow(link, callback=self.parse_items)
        #     yield txt_response
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_items(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroySpiderItem(), response=response)

        loader.add_css('name',
                       'span.t9jup0e_plp p1h8lbu4_plp::text')

        loader.add_css('photo',
                       'picture[class*="p10zxbd6_plp"]::attr(srcset)')

        loader.add_css('price', 'li.item-params-list-item::text')

        loader.add_value('url', response.url)

        loader.add_css('desc', '.pdp-section pdp-section--product-description::text')

        yield loader.load_item()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(LeroySpider)
process.start()
