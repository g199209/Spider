# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-23
# Brief  : 用于获取交大公司招聘宣讲会的爬虫
######################

import WebsiteBase
import requests, time, re, logging, sqlite3
from bs4 import BeautifulSoup


class SJTU_Talk(WebsiteBase.WebsiteBase):
    def __init__(self, Name, DBName, AgentID, KeyWords):
        super().__init__(Name, DBName, AgentID, True, KeyWords, 7)

    # Return number of pages
    def GetPageRange(self):
        return ['all', 'jt', 'mt', 'bz']

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        Formdata = {'xjhType': page}
        return requests.post('http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx',
                             data=Formdata, timeout=7)

    # Return soup
    def GetEnclose(self, soup):
        return soup.find('div', class_='z_newsl')

    # Return list of tag
    def GetTags(self, soup):
        tags = soup.find_all('li')
        del tags[0]
        return tags

    # Return title string
    def GetTitle(self, tag):
        if not tag.find('a').string:
            companyName = ''
            for s in tag.find('a').contents:
                companyName += s.string
        else:
            companyName = tag.find('a').string
        return re.sub(r'\s', '', companyName)

    # Return URL string
    def GetURL(self, tag):
        basecontentURL = 'http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=viewXjhxx&id='
        contentsuffix = tag.find('a')['onclick']
        contentsuffix = re.search(r"viewXphxx.'(\w+)'.", contentsuffix).group(1)
        contentURL = basecontentURL + contentsuffix
        return contentURL

    # Return publish time
    def GetPublishTime(self, tag):
        return ''

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        # Get time & Location
        talktime = tag.find_all('div')[3].string + ' ' + tag.find_all('div')[4].string
        talkloc = tag.find_all('div')[2].string
        # Generate BriefList
        BriefString = talktime + '\r\n' + talkloc + '\r\n\r\n' + keywordstring
        return BriefString