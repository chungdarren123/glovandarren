import scrapy
from ..items import ScrapedTextItem # Use the item
from datetime import datetime

class BasicSpider(scrapy.Spider):
    name = "basic_text_scraper"
    start_urls = [
        'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
        'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html',
    ]
    # No direct DB session needed in spider anymore

    def parse(self, response):
        page_title = response.css('title::text').get()

        item = ScrapedTextItem()
        item['url'] = response.url
        item['content'] = f"Title: {page_title}\nBody text could be extracted here using response.xpath('//p//text()').getall() or similar selectors."
        item['timestamp'] = datetime.utcnow() # Set timestamp here or in pipeline

        self.log(f"Scraped item from {response.url}")
        yield item
