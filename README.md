# 使用Python实现的网站变化监测系统

关于此系统实现方法和思路等可参考我的博客文章：
[使用Python实现网站变化监测系统](https://gaomf.cn/2016/07/26/%E4%BD%BF%E7%94%A8Python%E5%AE%9E%E7%8E%B0%E7%BD%91%E7%AB%99%E5%8F%98%E5%8C%96%E7%9B%91%E6%B5%8B%E7%B3%BB%E7%BB%9F/)

## 使用方法 ##
Python版本： Python 3.4 & Python 3.5测试通过，不兼容Python 2.x

依赖包：`requests`、`beautifulsoup4`

运行前需要将微信的`corpid`及`corpsecret`写入`wchat`文件中，此文件为文本文件，第一行是`corpid`，第二行是`corpsecret`，将此文件置于根目录下再运行`Spider.py`文件即可。

目前程序中检测的网站是按照我目前的需求添加的，可根据需要进行修改。

## 添加新网站 ##
复制`Template.py`文件，在此模板的基础上进行修改即可。

1.类名改为需要的名字

2.`__init__(self, Name, DBName, AgentID, KeyWords)`

子类的构造函数中调用了基类的构造函数，基类构造函数的参数说明如下：

```
# Name : 网站名称
# DBName ： 数据库名称，不要包含后缀
# AgentID ： 微信发布时需要用到的AgentID
# CheckContent ： 是否需要打开URL检查内容，True or False
# KeyWords : 过滤用关键词List，如果不需要设置为[]
# KeyWordsThreshold : 关键词阈值，内容页包含的关键词个数超过这个值才认为符合要求
# encoding ： 网站的编码格式，不设置的话默认为utf-8
__init__(self, Name, DBName, AgentID, CheckContent, KeyWords, KeyWordsThreshold, encoding = 'utf-8')
```

此构造函数的输入参数根据具体网站确定，可以一个参数都不用传入，全部固定下来，也可以添加一些其他需要的参数。

3.`GetPageRange(self)`

需要返回一个List，这个List中包含了需要采集的子页面的信息，可以是一些固定的字符串，也可以是一个range。如果只有一个页面，此处返回range(1)即可。

4.`GetMainPage(self, page)`

返回需要监测的页面，返回结果是由`requests.get()`方法返回的`response`对象。输入参数中的`page`就是之前`GetPageRange(self)`函数中返回的List中的元素，在需要监测多个页面的情况下根据此参数返回对应的页面即可。

5.`GetEnclose(self, soup)`

返回感兴趣的页面范围，输入参数`soup`是根据之前获取到的页面创建的`beautifulsoup`对象，此处也要返回一个`beautifulsoup`对象。最常见的情况是选取原始`soup`中的一个标签返回，如：

```
return soup.find('table')
```

如果不需要进行范围缩小，直接返回传入的`soup`即可。

6.`GetTags(self, soup)`

返回tag List，其中每一个元素都是一个`tag`，对应一条消息记录。此List一般通过`soup.find_all()`方法获得，不过某些情况下也需要手工生成，可以使用`soup.contents`等方法进行遍历后生成。

7.`GetTitle(self, tag)`

输入参数为一条消息记录对应的`tag`，需要从中找出标题信息并返回string，必须要返回一个string。

8.`GetURL(self, tag)`

输入参数为一条消息记录对应的`tag`，需要从中找出URL信息并返回string，可以返回`''`。

9.`GetPublishTime(self, tag)`

输入参数为一条消息记录对应的`tag`，需要从中找出发布日期信息并返回string，可以返回`''`。

10.`AdditionCheck(self, tag)`

输入参数为一条消息记录对应的`tag`，可对其进行一些额外的检查工作来判断此条消息是否是需要的消息，如果是需要的符合要求的消息则返回`True`，否则返回`False`。如果不需要判断直接返回`True`。

11.`GetBrief(self, tag, keywordstring)`

输入参数为一条消息记录对应的`tag`，之前关键词过滤结果`keywordstring`。如果进行了关键词过滤，`keywordstring`的格式类似于`*** 关键词： 关键词1；关键词2；`，如果没有进行关键词过滤，`keywordstring`为空。需要返回的是消息的摘要信息，如果不需要的话直接返回`''`即可。

----------

按上述方法添加好了网站子类后在`Spider.py`文件中实例化一个对象，并将其添加到`WebList`中即可~
