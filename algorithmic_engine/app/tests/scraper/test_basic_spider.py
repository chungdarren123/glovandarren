import pytest
from scrapy.http import HtmlResponse, Request
from app.scraper.spiders.basic_spider import BasicSpider
from app.scraper.items import ScrapedTextItem

@pytest.fixture
def spider():
    return BasicSpider()

def test_spider_parse(spider):
    # A minimal HTML body for testing title extraction
    body = "<html><head><title>Test Title</title></head><body><p>Some content.</p></body></html>"
    url = "http://fake-test-site.com/page1"
    request = Request(url=url)
    # The encoding is important for HtmlResponse
    response = HtmlResponse(url=url, request=request, body=body, encoding='utf-8')

    # The spider's parse method is a generator
    results = list(spider.parse(response))

    assert len(results) == 1
    item = results[0]
    assert isinstance(item, ScrapedTextItem)
    assert item['url'] == url
    assert "Title: Test Title" in item['content']
    assert item['timestamp'] is not None
