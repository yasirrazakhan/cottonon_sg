# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CottononSgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    images = scrapy.Field()
    category = scrapy.Field()
    variant = scrapy.Field()
    product_id = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()

