import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class VozScraper(CrawlSpider):
    name = 'voz'
    allow_domains = ['voz.vn']
    start_urls = ['https://voz.vn/f/chuyen-tro-linh-tinh.17/']

    rules = (
        Rule(LinkExtractor(allow = (r"f/chuyen-tro-linh-tinh.17/",),deny=r'/t/')),
        Rule(LinkExtractor(allow = (r"/t/",)), callback='parse_item'),
    )
    def parse_item(self, response):
        articles = response.xpath('//article[contains(@class, "message") and contains(@class, "message--post")]')
        #articles = response.css('article.message.message--post')
        limit = 0
        for article in articles:
            if limit >= 50:
                break
            author = article.css('.message-name a::text').get()
            message = article.css('.message-body .bbWrapper::text').getall()
            message = ' '.join([text.strip() for text in message if text.strip()])
            time = article.css('.u-dt::attr(datetime)').get()
            
            yield {
                'author': author,
                'message': message,
                'time': time
            }
            limit += 1
