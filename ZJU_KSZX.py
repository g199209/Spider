# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-21
# Brief  : 用于获取浙大考试中心网站新通知的爬虫
######################

import requests, time, re, logging, sqlite3
from bs4 import BeautifulSoup
import WebsiteBase


class ZJU_KSZX(WebsiteBase.WebsiteBase):
    def __init__(self, AgentID):
        super().__init__('浙大考试中心', 'ZJU_KSZX', AgentID, False, ['全国计算机等级考试'], 7)

    # Return number of pages
    def GetPageRange(self):
        return range(1)

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        return requests.get('http://kszx.zju.edu.cn/Default.aspx', timeout=21)

    # Return soup
    def GetEnclose(self, soup):
        return soup.find('div', id='main')

    # Return list of tag
    def GetTags(self, soup):
        return soup.find_all('tr')

    # Return title string
    def GetTitle(self, tag):
        return re.sub('[●\n ]', '', tag.find('a').contents[0].string)

    # Return URL string
    def GetURL(self, tag):
        return 'http://kszx.zju.edu.cn/' + tag.find('a')['href']

    # Return publish time
    def GetPublishTime(self, tag):
        return re.sub('[【】]', '', tag.find('font', color='lightgray').string)

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        return ''