import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from hsbc_tr.items import Article


class HsbcspiderSpider(scrapy.Spider):
    name = 'hsbcspider'
    allowed_domains = ['hsbc.com.tr']
    start_urls = ['https://www.hsbc.com.tr/haberler']

    def parse(self, response):
        links = response.xpath('//ul[@id="news"]/li/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="page-explanation"]/h1//text()').getall()
        title = " ".join(title).strip()

        content = response.xpath('//div[@class="SubPage-Container"]//text()').getall()
        content = [text for text in content if text.strip()]
        date = content.pop(0)
        content = "\n".join(content).strip()
        date = datetime.strptime(date, '%d.%m.%Y')
        date = date.strftime('%Y/%m/%d')

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
