import scrapy
import requests
from bs4 import BeautifulSoup,Comment
from selenium import webdriver
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import pymongo
import re
# from items import PrivacyItem

import json
def getPrivacy(url):
    ppurl =url
    # print('00000000000',ppurl)
    req = requests.get(ppurl)
    html = req.text
    soup = BeautifulSoup(html, "lxml")
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]
    b_text = soup.get_text()
    b_text.replace('\\n', ' ').replace('\\t', ' ')
    b_text = re.sub('\s+', ' ', b_text)
    # print(b_text)

    privacy_data={
        'url':ppurl,
        'text':b_text
    }
    getdb(privacy_data)
    print(privacy_data)
    return privacy_data

def getdb(privacy_data):
    client = pymongo.MongoClient('mongodb://root:root@127.0.0.1:27017')
    rent_info=client['ppvisual']
    sheet_table=rent_info['PrivacyItem']

    sheet_table.insert(privacy_data)

    # html_url = response.url
    # privacy_item['url'] = html_url
    # req = requests.get(url=html_url)
    # html = req.text
    # soup = BeautifulSoup(html, "lxml")
    # [x.extract() for x in soup.find_all('script')]
    # [x.extract() for x in soup.find_all('style')]
    # [x.extract() for x in soup.find_all('meta')]
    # [x.extract() for x in soup.find_all('noscript')]
    # [x.extract() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]
    # b_text = soup.get_text()
    # b_text.replace('\\n', ' ').replace('\\t', ' ')
    # b_text = re.sub('\s+', ' ', b_text)
    # privacy_item['text'] = b_text
    # yield privacy_item