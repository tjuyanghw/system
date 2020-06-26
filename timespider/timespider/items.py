# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TimespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    appname = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    size = scrapy.Field()
    download_num = scrapy.Field()
    cur_version = scrapy.Field()
    require = scrapy.Field()
    level = scrapy.Field()
    interaction = scrapy.Field()
    developer = scrapy.Field()
    dev_web = scrapy.Field()
    dev_email = scrapy.Field()
    dev_name = scrapy.Field()
    authority = scrapy.Field()
    review = scrapy.Field()
    privacy_policy = scrapy.Field()
    products = scrapy.Field()
    str = scrapy.Field()
    time = scrapy.Field()
    star = scrapy.Field()
    user = scrapy.Field()
    support = scrapy.Field()
    all_text = scrapy.Field()
    update = scrapy.Field()
    app_id = scrapy.Field()
    iap = scrapy.Field()


class ReviewItem(scrapy.Item):
    review = scrapy.Field()
    url = scrapy.Field()


class PrivacyItem(scrapy.Item):
    text = scrapy.Field()
    url = scrapy.Field()