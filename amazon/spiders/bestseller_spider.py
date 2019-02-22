import re
from urllib import parse

import scrapy

from amazon.items import Bestseller
from amazon.sql import Sql


class BestSellSpider(scrapy.Spider):

    name = "bestseller"
    allowed_domains = ["wwww.amazon.com"]

    """
    根据分类从数据库里面查询url
    """

    def start_requests(self):
        params = dict(
            category_title="toys-and-games"
        )
        urls = Sql.getBestsellerURL(params)
        for urlItem in urls:
            yield scrapy.Request(url=urlItem["url"], callback=self.parse)

    pass

    """
    解析当前页bestsellers的所有数据
    """
    def parse(self, response):
        list = response.xpath("//ol[@id='zg-ordered-list']/li")
        for item in list:
            bean = Bestseller()
            url = item.xpath(".//a[@class='a-link-normal']/@href").extract_first()
            bean['url'] = parse.urljoin(response.url, url)
            bean['title'] = item.xpath(".//a[@class='a-link-normal']/div[1]/text()").extract_first().strip()
            bean['ranks'] = item.xpath(".//span[@class='zg-badge-text']/text()").extract_first()
            bean['category'] = ""

            # 处理价格
            price = item.xpath(".//span[@class='p13n-sc-price']/text()").extract_first()
            if price is None:
                price = "0"
            else:
                price = price.replace("$", "")
            bean['price'] = price

            # 处理供货商数量
            offers = item.xpath(".//span[@class='a-color-secondary']/text()").extract_first()
            if offers:
                offers = "0"
            if offers is None:
                offers = "0"
            bean['offers'] = offers

            # 处理评论数量
            review = item.xpath(".//a[@class='a-size-small a-link-normal']/text()").extract_first()
            if review is None:
                review = "0"
            review = review.replace(",", "")
            bean['review'] = review

            # 处理asin码
            bean['asin'] = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)
            yield bean

    pass
