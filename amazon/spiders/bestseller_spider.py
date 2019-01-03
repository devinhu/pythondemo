import re
from urllib import parse

import scrapy
from scrapy.http import Request

from amazon.items import Bestseller
from amazon.items import BestsellerURL


class BestSellSpider(scrapy.Spider):
    name = "bestseller"
    allowed_domains = ["wwww.amazon.com"]
    start_urls = ["https://www.amazon.com/Best-Sellers/zgbs/"]

    """
    据URL解析当前关键字下的bestsellers的URL以及子类下面的URL
    """

    def parse(self, response):
        list = response.xpath("//*[@id='zg_browseRoot']/ul/li")
        for item in list:
            bean = BestsellerURL()
            bean['url'] = item.xpath("./a/@href").extract_first()
            bean['title'] = item.xpath("./a/text()").extract_first().strip()
            bean['parent_title'] = "amazon"
            yield bean
            yield Request(url=bean['url'], callback=self.parse_bestsellers_products, dont_filter=True)
            # yield Request(url=bean['url'], callback=self.parse_child1_url, dont_filter=True)

    pass

    """
    解析子分类
    """

    def parse_child1_url(self, response):
        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/li")
        for item in list:
            bean = BestsellerURL()
            bean['url'] = item.xpath("./a/@href").extract_first()
            bean['title'] = item.xpath("./a/text()").extract_first().strip()
            bean['parent_title'] = ""
            yield bean
            yield Request(url=bean['url'], callback=self.parse_child2_url, dont_filter=True)

    pass

    """
    解析子分类
    """

    def parse_child2_url(self, response):
        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/ul/li")
        for item in list:
            bean = BestsellerURL()
            bean['url'] = item.xpath("./a/@href").extract_first()
            bean['title'] = item.xpath("./a/text()").extract_first().strip()
            bean['parent_title'] = ""
            yield bean

    pass

    """
    解析当前页bestsellers的所有数据
    """

    def parse_bestsellers_products(self, response):
        list = response.xpath("//ol[@id='zg-ordered-list']/li")
        for item in list:
            bean = Bestseller()
            url = item.xpath(".//a[@class='a-link-normal']/@href").extract_first()
            bean['url'] = parse.urljoin(response.url, url)
            bean['title'] = item.xpath(".//a[@class='a-link-normal']/div[1]/text()").extract_first().strip()
            bean['ranks'] = item.xpath(".//span[@class='zg-badge-text']/text()").extract_first()

            price = item.xpath(".//span[@class='p13n-sc-price']/text()").extract_first()
            if price is None:
                price = "0"
            else:
                price = price.replace("$", "")
            bean['price'] = price

            offers = item.xpath(".//span[@class='a-color-secondary']/text()").extract_first()
            if offers:
                offers = "0"
            if offers is None:
                offers = "0"
            bean['offers'] = offers

            review = item.xpath(".//a[@class='a-size-small a-link-normal']/text()").extract_first()
            if review:
                review = "0"
            bean['review'] = review

            bean['asin'] = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)
            yield bean

    pass
