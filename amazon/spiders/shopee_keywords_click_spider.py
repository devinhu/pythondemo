import urllib
from urllib import parse
import scrapy
from scrapy.http import Request
import urllib
from urllib import parse

import scrapy
from scrapy.http import Request


class KeyWordsSpider(scrapy.Spider):
    name = "shopee_keywords_click"
    seed = "sofa"
    allowed_domains = ["shopee.com.my"]
    start_urls = ["https://shopee.com.my/search?keyword=casual%20bag"]

    """
    解析当前页bestsellers的所有数据
    """

    def parse(self, response):
        list = response.xpath(".//div[@class='col-xs-2-4 shopee-search-item-result__item']")
        for item in list:
            ad = item.xpath(".//div[@class='_2uCaTM']")
            if ad:
                url = item.xpath(".//a[@data-sqe='link']/@href").extract_first()
                url = parse.urljoin(response.url, url)
                url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
                print("url: " + url)
                i = 0
                while i <= 100:
                    i += 1
                    yield Request(url=response.url, callback=self.parse, dont_filter=True)
    pass
