# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-24
# Brief  : 用于获取复旦公司招聘宣讲会的爬虫
######################

import WebsiteBase
import requests, time, re, logging, sqlite3
from bs4 import BeautifulSoup


class FD_Talk(WebsiteBase.WebsiteBase):
    def __init__(self, Name, DBName, AgentID, KeyWords, SpecialKeyWords = []):
        super().__init__(Name, DBName, AgentID, True, KeyWords, 3, SpecialKeyWords)

    # Return number of pages
    def GetPageRange(self):
        return range(1)

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        payload = {'count': 100}
        return requests.get('http://www.career.fudan.edu.cn/jsp/career_talk_list.jsp', params=payload, timeout=21)

    # Return soup
    def GetEnclose(self, soup):
        return soup.find('div', id='tab1')

    # Return list of tag
    def GetTags(self, soup):
        return soup.find_all('div', id='tab1_bottom')

    # Return title string
    def GetTitle(self, tag):
        return tag.find_all('div')[0].string

    # Return URL string
    def GetURL(self, tag):
        basecontentURL = 'http://www.career.fudan.edu.cn/jsp/career_talk_detail.jsp?key='
        contentsuffix = tag['key']
        contentURL = basecontentURL + contentsuffix
        return contentURL

    # Return publish time
    def GetPublishTime(self, tag):
        return ''

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        if (tag.find_all('div')[0].string.count('已举办') > 0):
            return False
        else:
            return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        # Get time & Location
        talktime = tag.find_all('div')[2].string + ' ' + tag.find_all('div')[3].string
        talkloc = tag.find_all('div')[4].string
        # Generate BriefList
        BriefString = talktime + '\r\n' + talkloc + '\r\n\r\n' + keywordstring
        return BriefString
