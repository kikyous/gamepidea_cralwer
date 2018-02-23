import scrapy
from gamepedia_scrapy.items import GamepediaScrapyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class GamepediaSpider(CrawlSpider):
    name = 'gamepedia'
    allowed_domains = ['terraria-zh.gamepedia.com']
    start_urls = ['https://terraria-zh.gamepedia.com/Terraria_Wiki']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(deny=('\.php\?')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = GamepediaScrapyItem()
        item['name'] = response.css('#firstHeading::text').extract_first()
        item['content'] = response.css('#bodyContent').extract_first()
        return item
