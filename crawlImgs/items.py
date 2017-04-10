# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlimgsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    image_label = scrapy.Field()
    # image_fromPageTitle = scrapy.Field()
    image_fromURL = scrapy.Field()
    image_fromURLHost = scrapy.Field()
    image_height = scrapy.Field()
    image_width = scrapy.Field()
    image_crawDateTime = scrapy.Field(serializer=str)
    