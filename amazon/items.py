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
    category = scrapy.Field()
    country = scrapy.Field()

    def insert_sql(self):
        sql = """
               insert into bestsellerURL(title, url, category, country)
               VALUES(%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE url=VALUES(url), category=VALUES(category), country=VALUES(country)
             """

        params = (self["title"], self["url"], self["category"], self["country"])

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
    country = scrapy.Field()

    def insert_sql(self):
        sql = """
               insert into bestseller(title, price, url, asin, review, offers, ranks, category, country)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
               on duplicate key update title=values(title), price=values(price), url=values(url), review=values(review), offers=values(offers), ranks=values(ranks), category=values(category), country=values(country)
             """

        params = (
        self["title"], self["price"], self["url"], self["asin"], self["review"], self["offers"], self["ranks"],
        self["category"], self["country"])

        return sql, params

    pass


class KeyWords(scrapy.Item):
    asin = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    seed = scrapy.Field()
    keyword = scrapy.Field()

    def insert_sql(self):
        sql = """
               insert into keywords(asin, title, brand, url, seed, keyword)
               values(%s, %s, %s, %s, %s, %s)
               on duplicate key update asin=values(asin), title=values(title), brand=values(brand), url=values(url), seed=values(seed), keyword=values(keyword)
             """

        params = (self["asin"], self["title"], self["brand"], self["url"], self["seed"], self["keyword"])

        return sql, params

    pass


class AdTrack(scrapy.Item):
    asin = scrapy.Field()
    url = scrapy.Field()
    rankno = scrapy.Field()
    keyword = scrapy.Field()
    creattime = scrapy.Field()

    def insert_sql(self):
        sql = """
               insert into adTrack(asin, url, rankno, keyword, creattime)
               values(%s, %s, %s, %s, %s)
               on duplicate key update asin=values(asin), url=values(url), rankno=values(rankno), keyword=values(keyword), creattime=values(creattime)
             """

        params = (self["asin"], self["url"], self["rankno"], self["keyword"], self["creattime"])

        return sql, params

    pass
