import re
from urllib import parse

import scrapy
from scrapy.http import Request
from six.moves import urllib

from amazon.items import AdTrack


class AdTrackSpider(scrapy.Spider):
    name = "adtrack"
    seed = "Reusable food storage bags"
    allowed_domains = ["wwww.amazon.com"]
    start_urls = ["https://www.amazon.com/s?k=" + seed + "&ref=nb_sb_noss"]

    """
    解析当前页bestsellers的所有数据
    """

    def parse(self, response):
        list = response.xpath("//div[@class='s-result-list sg-row']/div")
        for item in list:
            bean = AdTrack()
            bean['keyword'] = self.seed

            url = item.xpath(".//a[@class='a-link-normal a-text-normal']/@href").extract_first()
            url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
            url = url.replace("-", " ")
            bean['url'] = parse.urljoin(response.url, url)

            bean['asin'] = re.match('.*/dp/(.*?)/ref.*', url, re.M | re.I).group(1)

            rankno = re.match('.*/ref=sr_(.*?)/?keywords.*', url, re.M | re.I).group(1)
            if rankno:
                rankno = rankno.replace("?", "")
                bean['rankno'] = rankno

            bean['creattime'] = "2019-03-11"

            yield bean

        nextURL = response.xpath("//li[@class='a-last']/a/@href").extract_first()
        if nextURL:
            nextURL = parse.urljoin(response.url, nextURL)
            yield Request(url=nextURL, callback=self.parse, dont_filter=True)

    pass
