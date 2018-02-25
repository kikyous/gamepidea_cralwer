# -*- coding: utf-8 -*-
import scrapy
from gamepedia_scrapy.items import GamepediaScrapyItem
from scrapy.http import Request

class GamepediaSpiderMain(scrapy.Spider):
    name = 'gamespider'
    root = 'https://terraria-zh.gamepedia.com'
    start_urls = [root+'/index.php?title=Special:所有页面&hideredirects=1']

    def fetch_item(self, response):
        item = GamepediaScrapyItem()
        item['name'] = response.css('#firstHeading::text').extract_first().replace(' ', '_')
        item['content'] = response.css('#bodyContent').extract_first()
        url = response.css('.interwiki-en a::attr(href)').extract_first()
        en_name = None
        if url:
            en_name = url.split('gamepedia.com/')[-1]

        item['en_name'] = en_name
        self.logger.info('%s', item['name'])
        return item

    def parse(self, response):
        for item in response.css('.mw-allpages-body li a::attr(href)').extract():
            yield Request(self.root + item + '?variant=zh-cn', callback=self.fetch_item)

        for next_page in response.css('div.mw-allpages-nav > a'):
            if u'下一页' in next_page.css('::text').extract_first():
                yield response.follow(next_page, self.parse)
                self.logger.info('Next page')
                break
