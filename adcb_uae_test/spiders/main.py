import scrapy
# from adcb_uae_test.items import Product
from lxml import html

class Adcb_uae_testSpider(scrapy.Spider):
    name = "adcb_uae_test"
    start_urls = ["https://example.com"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        print("Visited:", response.url)
