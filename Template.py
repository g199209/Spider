# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-25
# Brief  : 爬虫网站模板
######################

import WebsiteBase
import requests, re
from bs4 import BeautifulSoup


class Template(WebsiteBase.WebsiteBase):
    def __init__(self, Name, DBName, AgentID, KeyWords):
        super().__init__(Name, DBName, AgentID, True, KeyWords, 7, 'gb2312')

    # Return number of pages
    def GetPageRange(self):
        return range(1, 8)

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        return requests.get('%s' % page, timeout=7)

    # Return soup
    def GetEnclose(self, soup):
        return soup.find('table')

    # Return list of tag
    def GetTags(self, soup):
        return soup.find_all('tr')

    # Return title string
    def GetTitle(self, tag):
        return tag.find('a').string

    # Return URL string
    def GetURL(self, tag):
        return tag.find('a')['href']

    # Return publish time
    def GetPublishTime(self, tag):
        return tag.find('td', class_="date").string

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        # Generate Brief
        BriefString = keywordstring
        return BriefString