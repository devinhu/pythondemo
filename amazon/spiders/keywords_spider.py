import re
from urllib import parse

import scrapy
from scrapy.http import Request
from six.moves import urllib

from amazon.items import KeyWords


class KeyWordsSpider(scrapy.Spider):

    name = "keywords"
    seed = "bedside caddy"
    allowed_domains = ["www.amazon.co.uk"]
    start_urls = ["https://www.amazon.co.uk/s?k=bedside&ref=nb_sb_noss"]

    """
    解析当前页bestsellers的所有数据
    """

    def parse(self, response):
        list = response.xpath("//div[@class='s-result-list sg-row']/div")
        for item in list:
            bean = KeyWords()
            bean['seed'] = self.seed

            url = item.xpath(".//a[@class='a-link-normal a-text-normal']/@href").extract_first()
            url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
            url = url.replace("-", " ")
            bean['url'] = parse.urljoin(response.url, url)

            bean['asin'] = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)

            brand = item.xpath(".//div[@class='a-row a-size-base a-color-secondary']/span/text()").extract_first()
            if brand:
                brand = brand.replace("by ", "").lower().strip()
                bean['brand'] = brand
            if brand is None:
                brand = ""
                bean['brand'] = brand

            title = item.xpath(".//a[@class='a-link-normal a-text-normal']/span/text()").extract_first()
            title = title.lower().strip()
            if title and brand:
                bean['title'] = title.replace(brand, "")

            keyword = re.match('.*/(.*?)/dp.*', url, re.M | re.I).group(1)
            keyword = keyword.lower()
            if keyword:
                bean['keyword'] = keyword.replace(brand, "")

            yield bean

        nextURL = response.xpath("//li[@class='a-last']/a/@href").extract_first()
        if nextURL:
            nextURL = parse.urljoin(response.url, nextURL)
            yield Request(url=nextURL, callback=self.parse, dont_filter=True)
    pass
