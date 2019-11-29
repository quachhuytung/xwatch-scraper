# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor

class DongHoNamSpider(scrapy.Spider):
    name = 'dong-ho-nam'
    allowed_domains = ['xwatch.vn']
    start_urls = [
        'https://xwatch.vn/dong-ho-nam-pc85.html'
    ]

    def parse(self, response):
        products_url_container = LinkExtractor(restrict_css=".product_image").extract_links(response)
        for product_url_container in products_url_container:
            yield scrapy.Request(url=product_url_container.url, callback=self.parse_product_information)
        next_page_url_container = LinkExtractor(restrict_css=".next-page").extract_links(response)
        if next_page_url_container:
            yield scrapy.Request(url=next_page_url_container[0].url, callback=self.parse)
    
    def parse_product_information(self, response):
        product_title = " ".join(response.xpath("//h1[@itemprop='name']/text()").get().split())
        product_price = " ".join(response.xpath("//*[@id=\"price\"]/text()").get().split())
        product_table_key = list(map(lambda x: " ".join(x.split()), response.css(".title_charactestic::text").getall()))
        product_table_val = list(map(lambda x: " ".join(x.split()), response.css(".content_charactestic::text").getall()))
        product_attribs = dict(zip(product_table_key, product_table_val))
        yield {
            "product_title": product_title, 
            "product_price": product_price,
            "product_attribs": product_attribs,
        }
