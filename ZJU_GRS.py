# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-21
# Brief  : 用于获取浙大研究生院网站新通知的爬虫
######################

import requests, time, logging, sqlite3
from bs4 import BeautifulSoup
import WebsiteBase


class ZJU_GRS(WebsiteBase.WebsiteBase):
    def __init__(self, AgentID):
        super().__init__('浙大研究生院', 'ZJU_GRS', AgentID, False, [], 7)

    # Return number of pages
    def GetPageRange(self):
        return range(1)

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        return requests.get('http://grs.zju.edu.cn/redir.php?catalog_id=16313', timeout=21)

    # Return soup
    def GetEnclose(self, soup):
        return soup.find('ul', class_='cg-pic-news-list')

    # Return list of tag
    def GetTags(self, soup):
        return soup.find_all('li')

    # Return title string
    def GetTitle(self, tag):
        return tag.find('a', target='_blank').string

    # Return URL string
    def GetURL(self, tag):
        return 'http://grs.zju.edu.cn/' + tag.find('a', target='_blank')['href']

    # Return publish time
    def GetPublishTime(self, tag):
        return tag.find('span', class_='art-dateee').string

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        return tag.find('div', class_='art-summary1').string