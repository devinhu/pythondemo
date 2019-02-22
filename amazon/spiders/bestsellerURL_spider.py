import re

import scrapy
from scrapy.http import Request

from amazon.items import BestsellerURL


class BestsellerURLSpider(scrapy.Spider):
    name = "bestsellerurl"
    allowed_domains = ["wwww.amazon.com"]
    start_urls = ["https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers/zgbs/fashion/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Handmade/zgbs/handmade/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Health-Personal-Care/zgbs/hpc/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Garden-Outdoor/zgbs/lawn-garden/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Home-Improvement/zgbs/hi/ref=zg_bs_nav_0",
                  "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0"]

    """
    据URL解析当前关键字下的bestsellers的URL以及子类下面的URL
    """
    def parse(self, response):
        category_title = re.match('.*/zgbs/(.*?)/ref.*', response.url, re.M | re.I).group(1)
        # 获取下一页数据
        nextlist = response.xpath("//ul[@class='a-pagination']/li/a")
        if nextlist:
            for pageURL in nextlist:
                pagetext = pageURL.xpath("text()").extract_first()
                if pagetext == "1" or pagetext == "2":
                    bean = BestsellerURL()
                    bean['url'] = pageURL.xpath("@href").extract()
                    bean['title'] = category_title
                    bean['category_title'] = category_title
                    yield bean

        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/li")
        for item in list:
            url = item.xpath("./a/@href").extract_first()
            title = item.xpath("./a/text()").extract_first().strip()
            bean = BestsellerURL()
            bean['url'] = url
            bean['title'] = title
            bean['category_title'] = category_title

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
                    bean['category_title'] = response.meta["category_title"]
                    yield bean

        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/ul/li")
        for item in list:
            url = item.xpath("./a/@href").extract_first()
            title = item.xpath("./a/text()").extract_first().strip()
            bean = BestsellerURL()
            bean['url'] = url
            bean['title'] = title
            bean['category_title'] = response.meta["category_title"]

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
                    bean['category_title'] = response.meta["category_title"]
                    yield bean
    pass

