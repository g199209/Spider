# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-25
# Brief  : 用于获取应届生求职网招聘信息的爬虫
######################

import WebsiteBase
import requests, time, re, logging, sqlite3
from bs4 import BeautifulSoup


class YJS(WebsiteBase.WebsiteBase):
    def __init__(self, Name, DBName, AgentID, KeyWords, SpecialKeyWords = []):
        self.joblocstring = ''
        self.JobLoc = ['全国', '上海', '杭州', '浙江', '深圳', '广州', '南京', '苏州']
        super().__init__(Name, DBName, AgentID, True, KeyWords, 7, SpecialKeyWords, 'gb2312')

    # Number of Pages
    def GetPageRange(self):
        return range(1, 20)

    def GetMainPage(self, page):
        return requests.get('http://www.yingjiesheng.com/commend-fulltime-%s.html'%page, timeout=21)

    def GetEnclose(self, soup):
        return soup.find('table')

    def GetTags(self, soup):
        tags = []
        for t in soup.find_all('tr'):
            if t.get('class'):
                tags.append(t)
        return tags

    def GetTitle(self, tag):
        return tag.find('a').contents[-1].string

    def GetURL(self, tag):
        basecontentURL = 'http://www.yingjiesheng.com'
        contentsuffix = tag.find('a')['href']
        if re.match('http.*', contentsuffix):
            contentURL = contentsuffix
        else:
            contentURL = basecontentURL + contentsuffix
        return contentURL

    def GetPublishTime(self, tag):
        return tag.find('td', class_="date").string

    def AdditionCheck(self, tag):
        flagcount = 0

        loctag = tag.find('span', style='color: #008000;')
        if not loctag:
            self.joblocstring = ''
            return False
        else:
            self.joblocstring = loctag.string
        for loc in self.JobLoc:
            flagcount += self.joblocstring.count(loc)
        if flagcount == 0:
            return False
        else:
            return True

    def GetBrief(self, tag, keywordstring):
        # Get emphasis
        if tag.find('span', class_='emphasis'):
            emphasis = '[置顶] '
        else:
            emphasis = ''
        # Generate Brief
        BriefString = emphasis + self.joblocstring + '\r\n\r\n' + keywordstring
        return BriefString
