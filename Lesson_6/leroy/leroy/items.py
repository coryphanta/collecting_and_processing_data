# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def convert_to_int(string):
    integer = int(string.replace(' ', ''))
    return integer


def str_beautify(string):
    string = string.replace('\n', '').strip()
    return string


class LeroySpiderItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_to_int), output_processor=TakeFirst())
    _id = scrapy.Field()
    photo = scrapy.Field(input_processor=MapCompose())
    url = scrapy.Field(output_processor=TakeFirst())
    desc = scrapy.Field(input_processor=MapCompose(str_beautify))
