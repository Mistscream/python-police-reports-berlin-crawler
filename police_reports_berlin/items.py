# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoliceReportBerlinItem(scrapy.Item):
    # define the fields for your item here like:
    created = scrapy.Field()
    updated = scrapy.Field()
    timestamp = scrapy.Field()
    category = scrapy.Field()
    raw = scrapy.Field()
    text = scrapy.Field()
    text_pre_processed = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
