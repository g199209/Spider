# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-12-26
# Brief  : 软考
######################

import WebsiteBase
import requests, re
from bs4 import BeautifulSoup


class RuanKao(WebsiteBase.WebsiteBase):
    def __init__(self, AgentID):
        super().__init__('浙江软考', 'Ruankao', AgentID, False, ['2016年下半年'], 1, ['2016年下半年'])

    # Return number of pages
    def GetPageRange(self):
        return range(1)

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        return requests.get('http://www.zjrjks.org/interIndex.do?method=list2&curPage=1&dir=/rjksw/zcwj/hgry', timeout=21)

    # Return soup
    def GetEnclose(self, soup):
        return soup

    # Return list of tag
    def GetTags(self, soup):
        return soup.find_all('td', class_="dot02")

    # Return title string
    def GetTitle(self, tag):
        return tag.find('a').string

    # Return URL string
    def GetURL(self, tag):
        return 'http://www.zjrjks.org/' + tag.find('a')['href']

    # Return publish time
    def GetPublishTime(self, tag):
        return '0000-00-00'

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        return ''