import re

import scrapy
from scrapy.http import Request

from amazon.items import BestsellerURL


class BestsellerURLSpider(scrapy.Spider):

    name = "bestsellerurl"

    country = "UK"
    allowed_domains = ["www.amazon.co.uk"]
    start_urls = ["https://www.amazon.co.uk/Best-Sellers-Toys-Games/zgbs/kids/ref=zg_bs_nav_0",
                  "https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors/zgbs/sports/ref=zg_bs_nav_0",
                  "https://www.amazon.co.uk/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0",
                  "https://www.amazon.co.uk/Best-Sellers-Kitchen-Home/zgbs/kitchen/ref=zg_bs_nav_0"]

    """
    据URL解析当前关键字下的bestsellers的URL以及子类下面的URL
    """
    def parse(self, response):
        category = re.match('.*/zgbs/(.*?)/ref.*', response.url, re.M | re.I).group(1)
        # 获取下一页数据
        nextlist = response.xpath("//ul[@class='a-pagination']/li/a")
        if nextlist:
            for pageURL in nextlist:
                pagetext = pageURL.xpath("text()").extract_first()
                if pagetext == "1" or pagetext == "2":
                    bean = BestsellerURL()
                    bean['url'] = pageURL.xpath("@href").extract()
                    bean['title'] = category
                    bean['category'] = category
                    bean['country'] = self.country
                    yield bean

        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/li")
        for item in list:
            url = item.xpath("./a/@href").extract_first()
            title = item.xpath("./a/text()").extract_first().strip()
            bean = BestsellerURL()
            bean['url'] = url
            bean['title'] = title
            bean['category'] = category
            bean['country'] = self.country

            # 获取子类URL
            yield Request(url=url, callback=self.parse_child_url, meta=bean, dont_filter=True)
    pass

    """
    解析子分类
    """

    def parse_child_url(self, response):
        # 获取下一页数据
        nextlist = response.xpath("//ul[@class='a-pagination']/li/a")
        if nextlist:
            for pageURL in nextlist:
                pagetext = pageURL.xpath("text()").extract_first()
                if pagetext == "1" or pagetext == "2":
                    bean = BestsellerURL()
                    bean['url'] = pageURL.xpath("@href").extract()
                    bean['title'] = response.meta["title"]
                    bean['category'] = response.meta["category"]
                    bean['country'] = self.country
                    yield bean

        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/ul/li")
        for item in list:
            url = item.xpath("./a/@href").extract_first()
            title = item.xpath("./a/text()").extract_first().strip()
            bean = BestsellerURL()
            bean['url'] = url
            bean['title'] = title
            bean['category'] = response.meta["category"]
            bean['country'] = self.country

            # 获取子类URL
            yield Request(url=url, callback=self.parse_child2_url, meta=bean, dont_filter=True)

    pass

    """
    解析子分类
    """

    def parse_child2_url(self, response):
        # 获取下一页数据
        nextlist = response.xpath("//ul[@class='a-pagination']/li/a")
        if nextlist:
            for pageURL in nextlist:
                pagetext = pageURL.xpath("text()").extract_first()
                if pagetext == "1" or pagetext == "2":
                    bean = BestsellerURL()
                    bean['url'] = pageURL.xpath("@href").extract()
                    bean['title'] = response.meta["title"]
                    bean['category'] = response.meta["category"]
                    bean['country'] = self.country
                    yield bean
    pass

