# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class P101Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DokiSlimItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    engname = scrapy.Field()
    starid = scrapy.Field()
    pic = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


class DokiItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    engname = scrapy.Field()
    starid = scrapy.Field()
    epsdata = scrapy.Field()
    hometown = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    birthday = scrapy.Field()
