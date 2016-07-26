# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data   : 2016-07-22
# Brief  : 用于获取网站新通知的爬虫基类
######################

import requests, re, time, sqlite3, json, logging
from bs4 import BeautifulSoup


class WebsiteBase:
    def __init__(self, Name, DBName, AgentID, CheckContent, KeyWords, KeyWordsThreshold, encoding = 'utf-8'):
        self.Name = Name
        self.DBName = DBName + '.db'
        self.DBCheckedName = DBName + '_checked.db'
        self.AgentID = AgentID
        self.CheckContent = CheckContent
        self.KeyWords = KeyWords
        self.encoding = encoding
        self.KeyWordsThreshold = KeyWordsThreshold

        # Wchat ID & Password
        f = open('wchat')
        self.corpid = f.readline().strip()
        self.corpsecret = f.readline().strip()
        f.close()

        # Error Status
        self.err = False

        # Init DB
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'create table Articles (Title TEXT, Brief TEXT, URL TEXT, DATE TEXT, Published INTEGER)')
        except:
            pass
        cursor.close()
        conn.commit()
        conn.close()
        # Use this DB to record checked messages.
        conn = sqlite3.connect(self.DBCheckedName)
        cursor = conn.cursor()
        try:
            cursor.execute('create table URL (URL TEXT)')
        except:
            pass
        cursor.close()
        conn.commit()
        conn.close()

    def GET(self):
        returnErr = None
        # Open DB
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        conn2 = sqlite3.connect(self.DBCheckedName)
        cursor2 = conn2.cursor()

        logging.warning('Getting : ' + self.Name + '......')

        PageRange = self.GetPageRange()

        for p in PageRange:
            logging.warning('  Getting : ' + str(p))

            try:
                time.sleep(3)
                response = self.GetMainPage(p)
            except Exception as err:
                returnErr = err
                logging.error('    ' + repr(err))
                continue

            response.encoding = self.encoding
            soup = BeautifulSoup(response.text, 'html5lib')

            soup = self.GetEnclose(soup)
            tags = self.GetTags(soup)
            logging.warning('    Number of Pages : ' + str(len(tags)))

            for tag in tags:
                # Get Title
                Title = self.GetTitle(tag)
                if not Title:
                    continue

                # Get URL
                ContentURL = self.GetURL(tag)

                # Get time
                PublishTime = self.GetPublishTime(tag)

                # Check DB
                cursor2.execute(
                    "select * from URL where URL = ?",
                    [(ContentURL)]
                )
                # Already exists
                if cursor2.fetchone():
                    continue

                # Addition Check
                if not self.AdditionCheck(tag):
                    continue

                if self.KeyWords:
                    # Check Title
                    flagcount = 0
                    keywordstring = ' 关键词：'
                    for keyword in self.KeyWords:
                        if (Title.count(keyword) > 0):
                            flagcount += Title.count(keyword)
                            keywordstring = keywordstring + keyword + '；'

                    if flagcount == 0 and not self.CheckContent:
                        # Next Title
                        continue

                    # Check Content
                    if flagcount == 0 and ContentURL != '':
                        try:
                            time.sleep(3)
                            response = requests.get(ContentURL, timeout=7)
                        except Exception as err:
                            returnErr = err
                            logging.error('    ' + repr(err))
                            continue

                        for keyword in self.KeyWords:
                            if (response.text.count(keyword)) > 0:
                                flagcount += response.text.count(keyword)
                                keywordstring = keywordstring + keyword + '；'

                        # Update Checked DB
                        cursor2.execute(
                            "insert into URL (URL) values (?)",
                            [(ContentURL)]
                        )
                        if flagcount < self.KeyWordsThreshold:
                            # Next Title
                            continue

                # Get Brief
                if self.KeyWords:
                    BriefString = self.GetBrief(tag, str(flagcount) + keywordstring)
                else:
                    BriefString = self.GetBrief(tag, '')

                # Update DB
                cursor.execute(
                    "select * from Articles where Title = ? and Brief = ? and URL = ? and DATE = ?",
                    (Title, BriefString, ContentURL, PublishTime)
                )
                # Already exist
                if cursor.fetchone():
                    continue

                cursor.execute(
                    "insert into Articles (Title, Brief, URL, DATE, Published) values (?, ?, ?, ?, ?)",
                    (Title, BriefString, ContentURL, PublishTime, 0)
                )
                logging.warning('    Updating : ' + Title + '......')

        # Close DB
        cursor.close()
        conn.commit()
        conn.close()
        cursor2.close()
        conn2.commit()
        conn2.close()

        if returnErr:
            raise returnErr

    def Update(self):
        logging.warning('Updating : ' + self.Name + '......')

        # Init Wchat
        access_token = self.InitWchat()
        if not access_token:
            return

        # Open DB
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()

        cursor.execute("select * from Articles where Published = 0")
        unpublished = cursor.fetchall()

        for record in unpublished:
            # Publish
            logging.warning('  Publishing : ' + record[0] + '......')

            newsdata = {'touser': '@all',
                        'msgtype': 'news',
                        'agentid': self.AgentID,
                        'news': {'articles': [{
                            'title': record[0],
                            'description': record[1],
                            'url': record[2]
                        }]}}

            try:
                time.sleep(1)
                r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', params=access_token,
                                  data=json.dumps(newsdata, ensure_ascii=False).encode('utf-8'), timeout=7)
            except:
                logging.error('Publish Timeout!')

            if 'errcode' in r.json() and r.json()['errcode'] == 0:
                logging.warning('    Publish Success!')
                cursor.execute("update Articles set Published = 1 where Title = ? and URL = ? and DATE = ?",
                               (record[0], record[2], record[3]))
            else:
                logging.error('Publish Error!')
                logging.error(json.dumps(newsdata, ensure_ascii=False))
                logging.error(r.json())

        # Close DB
        cursor.close()
        conn.commit()
        conn.close()

    def ReportErrStatus(self, errstr):
        access_token = self.InitWchat()
        if not access_token:
            return

        if self.err:
            newsdata = {'touser': 'g199209',
                        'msgtype': 'news',
                        'agentid': 0,
                        'news': {'articles': [{
                            'title': '云端程序错误',
                            'description': self.Name + ' :\r\n' + errstr,
                        }]}}
        else:
            newsdata = {'touser': 'g199209',
                        'msgtype': 'news',
                        'agentid': 0,
                        'news': {'articles': [{
                            'title': '云端程序正常运行',
                            'description': self.Name + ' :\r\n云端程序已从上次错误中恢复，现已正常运行~',
                        }]}}

        try:
            r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', params=access_token,
                              data=json.dumps(newsdata, ensure_ascii=False).encode('utf-8'), timeout=7)
        except:
            logging.error('Send Wchat Report Timeout!')

    def InitWchat(self):
        # Init Wchat
        Auth = {'corpid': self.corpid,
                'corpsecret': self.corpsecret}
        try:
            r = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', params=Auth, timeout=7)
        except:
            logging.error('Wchat Init Timeout!!')
            return None

        if 'access_token' in r.json():
            return {'access_token': r.json()['access_token']}
        else:
            logging.error('Wchat Init Error!!')
            return None

    def GetPageRange(self):
        pass

    def GetMainPage(self, page):
        pass

    def GetEnclose(self, soup):
        pass

    def GetTags(self, soup):
        pass

    def GetTitle(self, tag):
        pass

    def GetURL(self, tag):
        pass

    def GetPublishTime(self, tag):
        pass

    def AdditionCheck(self, tag):
        pass

    def GetBrief(self, tag, keywordstring):
        pass

