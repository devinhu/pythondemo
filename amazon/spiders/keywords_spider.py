import re
from urllib import parse

import scrapy
from six.moves import urllib

from amazon.items import KeyWords


class KeyWordsSpider(scrapy.Spider):
    name = "keywords"
    allowed_domains = ["wwww.amazon.com"]
    start_urls = ["https://www.amazon.com/s?k=3d+pen&ref=nb_sb_noss_2"]

    """
    解析当前页bestsellers的所有数据
    """

    def parse(self, response):
        list = response.xpath("//div[@class='s-result-list sg-row']/div")
        for item in list:
            bean = KeyWords()
            bean['keytitle'] = "3d pen"

            url = item.xpath(".//a[@class='a-link-normal a-text-normal']/@href").extract_first()
            url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
            url = url.replace("-", " ")

            bean['url'] = parse.urljoin(response.url, url)
            bean['asin'] = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)
            bean['title'] = item.xpath(".//a[@class='a-link-normal a-text-normal']/span/text()").extract_first().strip()
            bean['keyletter'] = re.match('.*/(.*?)/dp.*', url, re.M | re.I).group(1)

            yield bean

    pass
