# -*- coding:utf-8 -*-

import requests
import re

Header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate'
}
#创建贴吧类
class TieBaInfo(object):

    def __init__(self,URL):
        self.HeadURL = URL

    #获取首页
    def GetFirstPageFun(self):

        #FirstPageUrl = 'http://tieba.baidu.com/mo/m?kw=%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6&lm=&pn=0'
        FirstPageUrl = 'http://tieba.baidu.com/mo/m?kw=%s&lm=&pn=0'%self.HeadURL
        GetFirstPage = requests.get(FirstPageUrl,headers = Header)
        GetFirstPage.encoding = 'utf-8'
        print GetFirstPage.text
        di = u'第'
        self.PageNumber = re.findall(r'%s1\/(\d*)'%di,GetFirstPage.text)[0]


tieba = TieBaInfo('%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6')
tieba.GetFirstPageFun()
print tieba.PageNumber




