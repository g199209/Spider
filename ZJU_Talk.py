# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-23
# Brief  : 用于获取浙大公司招聘宣讲会的爬虫
######################

import WebsiteBase
import requests, time, re, logging, sqlite3
from bs4 import BeautifulSoup


class ZJU_Talk(WebsiteBase.WebsiteBase):
    def __init__(self, Name, DBName, AgentID, KeyWords):
        super().__init__(Name, DBName, AgentID, True, KeyWords, 7, 'gb2312')

    # Return number of pages
    def GetPageRange(self):
        # Get Number of Pages
        Formdata = {'pages.currentPage': 1,
                    'zphlx': 0,
                    'pages.pageSize': 30
                    }
        r = requests.post('http://www.career.zju.edu.cn/ejob/zczphxxmorelogin.do', data=Formdata, timeout=10)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, 'html5lib')
        NofPages = int(soup.find('span', title='总页数').contents[0].string)
        if (NofPages > 7):
            NofPages = 7
        self.NofPages = 7
        return range(1, NofPages + 1)

    # Use requests to get the main page, return response
    def GetMainPage(self, page):
        Formdata = {'pages.currentPage': page,
                    'pages.maxPage': self.NofPages,
                    'zphlx': 0,
                    'pages.pageSize': 30
                    }
        return requests.post('http://www.career.zju.edu.cn/ejob/zczphxxmorelogin.do',
                             data=Formdata, timeout=10)

    # Return soup
    def GetEnclose(self, soup):
        return soup

    # Return list of tag
    def GetTags(self, soup):
        return soup.find_all('tr', class_='con')

    # Return title string
    def GetTitle(self, tag):
        # Get Company Name
        if not tag.find('a').string:
            companyName = ''
            for s in tag.find('a').contents:
                companyName += s.string
        else:
            companyName = tag.find('a').string
        companyName = re.sub(r'\s', '', companyName)
        return companyName

    # Return URL string
    def GetURL(self, tag):
        return 'http://www.career.zju.edu.cn/ejob/' + tag.find('a')['href']

    # Return publish time
    def GetPublishTime(self, tag):
        return ''

    # Addditon check, return True if unused
    def AdditionCheck(self, tag):
        return True

    # Return brief string
    def GetBrief(self, tag, keywordstring):
        # Get time & Location
        retmp = re.search(r'\s*([0-9\-]+)\s*([0-9:]+).*', tag.find_all('td')[2].string)
        talktime = retmp.group(1) + ' ' + retmp.group(2)
        talkloc = re.sub(r'\s', '', tag.find_all('td')[1].string)
        # Generate BriefList
        BriefString = talktime + '\r\n' + talkloc + '\r\n\r\n' + keywordstring
        return BriefString