import scrapy, time

class AltwallSpider(scrapy.Spider):
    name = 'altwall'
    allowed_domains = ['altwall.net']
    start_urls = ['https://altwall.net/genres.php?show=111']

    def parse(self, response):
        for title in response.xpath('//*[contains(@class, "underline")]'):
            yield {'title': title.xpath('text()').extract_first()}