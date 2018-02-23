# -*- coding: utf-8 -*-
import re
import scrapy
from gamepedia_scrapy.items import GamepediaScrapyItem
from scrapy.http import Request


import scrapy

class GamepediaSpiderMain(scrapy.Spider):
    name = 'gamespider_changes'
    start_urls = ['https://terraria-zh.gamepedia.com/index.php?title=Special:%E6%9C%80%E8%BF%91%E6%9B%B4%E6%94%B9&limit=250']

    def fetch_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = GamepediaScrapyItem()
        item['name'] = response.css('#firstHeading::text').extract_first()
        item['content'] = response.css('#bodyContent').extract_first()
        return item

    def parse(self, response):
        root = 'https://terraria-zh.gamepedia.com'
        for item in response.css('a.mw-changeslist-title::attr(href)').extract():
            if not re.match('/index|/User|/Terraria_Wiki|/Template|/MediaWiki', item):
                print(item)
                yield Request(root + item, callback=self.fetch_item)
