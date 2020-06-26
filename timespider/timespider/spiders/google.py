# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup,Comment
from selenium import webdriver
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import json
import urllib
import re
from ..privacySpider import getPrivacy
#scrapy.Spider
from ..items import TimespiderItem,ReviewItem,PrivacyItem
class GoogleSpider(CrawlSpider):
    name = 'google'
    allowed_domains = ['play.google.com']
    start_urls = [
        'https://play.google.com/store/apps/details?id=com.visiblebody.atlas'
    #     'https://play.google.com/store/apps/details?id=com.facebook.orca',
    # 'https://play.google.com/store/apps/details?id=com.ss.android.article.topbuzzvideo',
    # 'https://play.google.com/store/apps/details?id=com.whatsapp',
    #     'https://play.google.com/store/apps/details?id=com.scb.phone'
             ]
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details",)),
             callback='parse_app', follow=True), ]
    # def __init__(self):
    #     # super(GoogleSpider, self).__init__(*args, **kwargs)
    #     # chrome_options = webdriver.ChromeOptions()
    #     # chrome_options.add_argument('lang=en-GB')
    #     # chrome_options.add_argument('--headless')
    #     # self.driver = webdriver.Chrome(chrome_options=chrome_options)
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.add_argument('lang=en-GB')
    #     prefs = {"profile.managed_default_content_settings.images": 2, "int1.accept_language": "en-GB"}
    #     chrome_options.add_experimental_option('prefs', prefs)
    #     self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def parse_app(self, response):
        # 在这里只获取页面的 URL 以及下载数量
        item = TimespiderItem()
        item['url'] = response.url

        app_id = response.url.split('=')[-1]

        if app_id:
            item['app_id'] = app_id
        else:
            item['app_id'] = ''
        appname = response.xpath(
            '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/c-wiz[1]/h1/span/text()').extract()[0]

        # 类别
        categories = response.xpath(
            '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div/div[1]/div[1]/span[2]/a/text()').extract()[0]
        #描述
        # description = response.xpath(
            # '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[4]/div/div[1]/div[2]/div[1]/span/div/text()').extract()
        description = response.xpath('//*[@id="fcxH9b"]//meta[@itemprop="description"]/@content').extract()
        if len(description):
            if str(description[0].encode('utf-8')) == 'Translate':
                description.pop(0)
        description = '`'.join(description)
        #评分
        rating = dict()
        rating['overall'] = response.xpath('//*[@id="fcxH9b"]//div[@class="BHMmbe"]/text()').extract()
        if (len(rating['overall']) > 0):
            rating['overall'] = rating['overall'][0]
        else:
            rating['overall'] = "0"
        ratings = response.xpath('//span[@title]//@title').extract()
        if (len(ratings) > 0):
            rating['five_star'] = ratings[0]
        else:
            rating['five_star'] = "0"
        if (len(ratings) > 1):
            rating['four_star'] = ratings[1]
        else:
            rating['four_star'] = "0"
        if (len(ratings) > 2):
            rating['three_star'] = ratings[2]
        else:
            rating['three_star'] = "0"
        if (len(ratings) > 3):
            rating['two_star'] = ratings[3]
        else:
            rating['two_star'] = "0"
        if (len(ratings) > 4):
            rating['one_star'] = ratings[4]
        else:
            rating['one_star'] = "0"
        rating["total_rating"] = response.xpath('//span[@aria-label]/text()').extract()

        if (len(rating['total_rating']) > 0):
            rating['total_rating'] = rating['total_rating'][0]
        else:
            rating['total_rating'] = "0"
        #更新日期
        item['update'] = response.xpath('//div[contains(text(),"Updated")]/..//span/text()').extract()
        if (len(item['update']) > 0):
            item['update'] = item['update'][0]
        else:
            item['update'] = ""
        #大小
        item['size'] = response.xpath('//div[contains(text(),"Size")]/..//span/text()').extract()
        if (len(item['size']) > 0):
            item['size'] = item['size'][0]
        else:
            item['size'] = ""
        #下载人数
        item['download_num'] = response.xpath('//div[contains(text(),"Installs")]/..//span/text()').extract()
        if (len(item['download_num']) > 0):
            item['download_num'] = item['download_num'][0]
        else:
            item['download_num'] = ""
        #版本
        item['cur_version'] = response.xpath('//div[contains(text(),"Current Version")]/..//span/text()').extract()
        if (len(item['cur_version']) > 0):
            item['cur_version'] = item['cur_version'][0]
        else:
            item['cur_version'] = ""
        #要求
        item['require'] = response.xpath('//div[contains(text(),"Requires Android")]/..//span/text()').extract()
        if (len(item['require']) > 0):
            item['require'] = item['require'][0]
        else:
            item['require'] = ""
        #内容分级
        item['level'] = response.xpath('//div[contains(text(),"Content Rating")]/../span//div/text()').extract()
        if (len(item['level']) > 0):
            item['level'] = '`'.join(item['level'])
        else:
            item['level'] = ""
        #互动
        item['interaction'] = response.xpath('//div[contains(text(),"Interactive Elements")]/..//span/text()').extract()
        if (len(item['interaction']) > 0):
            item['interaction'] = item['interaction'][0]
        else:
            item['interaction'] = ""
        #价值
        item['iap'] = response.xpath('//div[contains(text(),"In-app Products")]/..//span/text()').extract()
        if (len(item['iap']) > 0):
            item['iap'] = item['iap'][0]
        else:
            item['iap'] = "0"
        #开发网站
        item['dev_web'] = response.xpath('//div[contains(text(),"Developer")]/..//a/@href').extract()
        if (len(item['dev_web']) > 0):
            item['dev_web'] = item['dev_web'][0]
        else:
            item['dev_web'] = ""
        #开发人员Email
        item['dev_email'] = response.xpath('//div[contains(text(),"Developer")]/..//a/@href').extract()
        if (len(item['dev_email']) > 2):
            item['dev_email'] = item['dev_email'][1]
        else:
            item['dev_email'] = ""
        #开发人员名字
        item['dev_name'] = response.xpath('//div[contains(text(),"Developer")]/..//div/text()').extract()
        if (len(item['dev_name']) > 0):
            item['dev_name'][0] = ""
            item['dev_name'] = ''.join(item['dev_name'])
        else:
            item['dev_name'] = ""
        #隐私地址
        item["privacy_policy"] = response.xpath(
            '//div[contains(text(),"Developer")]/..//a[contains(text(),"Privacy Policy")]/@href').extract()
        if (len(item["privacy_policy"]) > 0):
            item["privacy_policy"] = item["privacy_policy"][0]
        else:
            item["privacy_policy"] = ""
        privacy_url = item["privacy_policy"]
        # pp_url = privacy_url[7:]
        # ppUrl = 'https://'+pp_url
        getPrivacy(privacy_url)
        item['appname'] = appname
        item['categories'] = categories
        item['description'] = description
        item["rating"] = "one_star:" + rating["one_star"] + ";" + "two_star:" + rating[
            "two_star"] + ";" + "three_star:" + rating["three_star"] + ";" + "four_star:" + rating[
                             "four_star"] + ";" + "five_star:" + rating["five_star"] + ";" + "total_rating:" + rating[
                             "total_rating"] + ";" + "overall:" + rating["overall"]
        # yield Request(url=ppUrl, callback=self.getPrivacy, dont_filter=True)
        yield item


        # yield Request(url=url + '&showAllReviews=true', callback=self.getReviews, dont_filter=True)



    # def getReviews(self, response):
    #
    #     item = ReviewItem()
    #     url = response.url
    #     self.driver.get(url)
    #     url = urllib.parse.urlsplit(url).query.split('&')[0].split('=')[-1]
    #     url1 = 'https://play.google.com/store/apps/details?id=' + url
    #     review_element_list = self.driver.find_elements_by_xpath(
    #         '//div[@jsname="fk8dgd"]//div[@jscontroller="H6eOGe"]//span[@jsname="bN97Pc"]')
    #     if len(review_element_list) > 0:
    #         for i in range(0, 5):
    #             js = "var q=document.documentElement.scrollTop=100000"
    #             self.driver.execute_script(js)
    #             time.sleep(2)
    #         try:
    #             show_more = self.driver.find_element_by_xpath('//span[contains(text(),"Show More")]')
    #             flag = True
    #         except:
    #             show_more = ""
    #             flag = False
    #
    #         while (flag):
    #             time.sleep(3)
    #             # show_more.click()
    #             self.driver.execute_script('arguments[0].click();', show_more)
    #             for i in range(0, 5):
    #                 js = "var q=document.documentElement.scrollTop=100000"
    #                 self.driver.execute_script(js)
    #                 time.sleep(2)
    #                 try:
    #                     show_more = self.driver.find_element_by_xpath('//span[contains(text(),"Show More")]')
    #                     flag = True
    #                 except:
    #                     flag = False
    #         full_reviews_len = len(self.driver.find_elements_by_class_name('OzU4dc'))
    #         if (full_reviews_len > 0):
    #             for j in range(0, full_reviews_len):
    #                 click_full_reviews = "var a = document.getElementsByClassName(\"" + 'OzU4dc' + "\"); a[" + str(
    #                     j) + "].click();"
    #                 self.driver.execute_script(click_full_reviews)
    #         review_list = []
    #
    #         reviews = self.driver.find_elements_by_class_name('d15Mdf')
    #
    #         for element in reviews:
    #             s = dict()
    #             s['name'] = element.find_element_by_class_name('X43Kjb').text
    #
    #             s['date'] = element.find_element_by_class_name('p2TkOb').text
    #
    #             s['rate'] = len(element.find_elements_by_class_name('vQHuPe'))
    #
    #             s['comment'] = element.find_element_by_class_name('UD7Dzf').text
    #
    #             s['helpful'] = element.find_element_by_class_name('jUL89d').text
    #
    #             s = json.dumps(s)
    #             review_list.append(s)
    #     else:
    #         review_list = ""
    #
    #     item['review'] = review_list
    #     item['url'] = url1
    #     yield item

    # def getPrivacy(self, response):
    #     privacy_item = PrivacyItem()
    #     html_url = response.url
    #     privacy_item['url'] = html_url
    #     req = requests.get(url=html_url)
    #     html = req.text
    #     soup = BeautifulSoup(html, "lxml")
    #     [x.extract() for x in soup.find_all('script')]
    #     [x.extract() for x in soup.find_all('style')]
    #     [x.extract() for x in soup.find_all('meta')]
    #     [x.extract() for x in soup.find_all('noscript')]
    #     [x.extract() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]
    #     b_text = soup.get_text()
    #     b_text.replace('\\n', ' ').replace('\\t', ' ')
    #     b_text = re.sub('\s+', ' ', b_text)
    #     privacy_item['text'] = b_text
    #     yield privacy_item