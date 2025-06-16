import scrapy

class ScrapedTextItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    timestamp = scrapy.Field() # Can be set in pipeline or spider
