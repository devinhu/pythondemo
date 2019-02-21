import re
from urllib import parse

import scrapy
from amazon.items import Bestseller


class BestSellSpider(scrapy.Spider):
    name = "bestseller"
    allowed_domains = ["wwww.amazon.com"]
    start_urls = ["https://www.amazon.com/Best-Sellers-Home-Kitchen-Bedding/zgbs/home-garden/1063252/ref=zg_bs_nav_hg_1_hg/147-8190480-3533248",
                "https://www.amazon.com/Best-Sellers-Home-Kitchen-Bath-Products/zgbs/home-garden/1063236/ref=zg_bs_nav_hg_1_hg/147-8190480-3533248"]


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
            if review is None:
                review = "0"
            review = review.replace(",", "")
            bean['review'] = review

            bean['asin'] = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)
            yield bean

    pass
