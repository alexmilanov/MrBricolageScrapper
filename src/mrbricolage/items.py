# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MrbricolageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    images = Field()
    image_url = Field()
