
import scrapy
from scrapy.http import Request

from amazon.items import BestsellerURL


class BestSellSpider(scrapy.Spider):
    parent_title = "Home & Kitchen"
    name = "bestsellerURL"
    allowed_domains = ["wwww.amazon.com"]
    start_urls = ["https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0"]

    """
    据URL解析当前关键字下的bestsellers的URL以及子类下面的URL
    """

    def parse(self, response):
        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/li")
        for item in list:
            bean = BestsellerURL()
            bean['url'] = item.xpath("./a/@href").extract_first()
            bean['title'] = item.xpath("./a/text()").extract_first().strip()
            bean['parent_title'] = self.parent_title
            yield bean
            # yield Request(url=bean['url'], callback=self.parse_bestsellers_products, dont_filter=True)
            yield Request(url=bean['url'], callback=self.parse_child1_url, meta=bean, dont_filter=True)

    pass


    """
    解析子分类
    """

    def parse_child1_url(self, response):
        list = response.xpath("//*[@id='zg_browseRoot']/ul/ul/ul/li")
        for item in list:
            bean = BestsellerURL()
            bean['url'] = item.xpath("./a/@href").extract_first()
            bean['title'] = item.xpath("./a/text()").extract_first().strip()
            bean['parent_title'] = response.meta["parent_title"]
            yield bean

    pass
