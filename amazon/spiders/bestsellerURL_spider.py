
import scrapy
from scrapy.http import Request

from amazon.items import BestsellerURL


class BestsellerURLSpider(scrapy.Spider):
    name = "bestsellerurl"
    allowed_domains = ["wwww.amazon.com"]

    title = "Toys & Games"
    start_urls = ["https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0"]

    """
    据URL解析当前关键字下的bestsellers的URL以及子类下面的URL
    """

    def parse(self, response):
        # 获取下一页数据
        nextlist = response.xpath("//ul[@class='a-pagination']/li/a")
        if nextlist:
            for pageURL in nextlist:
                pagetext = pageURL.xpath("text()").extract_first()
                if pagetext == "1" or pagetext == "2":
                    bean = BestsellerURL()
                    bean['url'] = pageURL.xpath("@href").extract()
                    bean['title'] = self.title
                    bean['category_title'] = self.title
                    yield bean

        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/li")
        for item in list:
            url = item.xpath("./a/@href").extract_first()
            title = item.xpath("./a/text()").extract_first().strip()
            bean = BestsellerURL()
            bean['url'] = url
            bean['title'] = title

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
                    bean['category_title'] = self.title
                    yield bean

        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/ul/li")
        for item in list:
            url = item.xpath("./a/@href").extract_first()
            title = item.xpath("./a/text()").extract_first().strip()
            bean = BestsellerURL()
            bean['url'] = url
            bean['title'] = title

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
                    bean['category_title'] = self.title
                    yield bean
    pass

