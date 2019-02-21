# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BestsellerURL(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    parent_title = scrapy.Field()

    def insert_sql(self):
        sql = """
               insert into bestsellerURL(title, url, parent_title)
               VALUES(%s, %s, %s)
               ON DUPLICATE KEY UPDATE url=VALUES(url), parent_title=VALUES(parent_title)
             """

        params = (self["title"], self["url"], self["parent_title"])

        return sql, params

    pass


class Bestseller(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    asin = scrapy.Field()
    review = scrapy.Field()
    offers = scrapy.Field()
    ranks = scrapy.Field()
    category = scrapy.Field()

    def insert_sql(self):
        sql = """
               insert into bestseller(title, price, url, asin, review, offers, ranks, category)
               values(%s, %s, %s, %s, %s, %s, %s, %s)
               on duplicate key update title=values(title), price=values(price), url=values(url), review=values(review), offers=values(offers), ranks=values(ranks), category=values(category)
             """

        params = (self["title"], self["price"], self["url"], self["asin"], self["review"], self["offers"], self["ranks"], self["category"])

        return sql, params

    pass
