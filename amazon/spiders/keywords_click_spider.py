import re
import urllib
from urllib import parse

import scrapy
from scrapy.http import Request


class KeyWordsSpider(scrapy.Spider):
    name = "keywords_click"
    seed = "bedside"
    allowed_domains = ["www.amazon.co.uk"]
    start_urls = ["https://www.amazon.co.uk/s?k=bedside"]

    """
    解析当前页bestsellers的所有数据
    """

    def parse(self, response):
        list = response.xpath(".//div[@data-component-type='sp-sponsored-result']")
        for item in list:
            url = item.xpath(".//a[@class='a-link-normal a-text-normal']/@href").extract_first()
            url = parse.urljoin(response.url, url)
            url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
            asin = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)
            print(asin)

            i = 0
            while i <= 100:
                i += 1
                yield Request(url=url, callback=self.parse, dont_filter=True)

        #
        # nextURL = response.xpath("//li[@class='a-last']/a/@href").extract_first()
        # if nextURL:
        #     nextURL = parse.urljoin(response.url, nextURL)
        #     yield Request(url=nextURL, callback=self.parse, dont_filter=True)

    pass
