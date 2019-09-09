# -*- coding: utf-8 -*-

import json
import codecs

JSON_FILE_NAME = 'mr_bricolage_data.json'
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MrbricolagePipeline(object):
    def __init__(self):
        self.file = codecs.open(JSON_FILE_NAME, 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
