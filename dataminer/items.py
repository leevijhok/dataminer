"""Defines scraped items. """

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# eBay Items:
class Product(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    approx_price = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()

class DataminerItem(scrapy.Item):

    # TODO: Add fields:
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
