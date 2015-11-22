# -*- coding:utf-8 -*-

import requests
import re

Header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate'
}

di = u'第'
lou = u'楼'

#贴吧类
class TieBaInfo(object):

    def __init__(self,URL):
        self.HeadURL = URL

    #获取首页
    def GetFirstPageFun(self):

        #FirstPageUrl = 'http://tieba.baidu.com/mo/m?kw=%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6&lm=&pn=0'
        FirstPageUrl = 'http://tieba.baidu.com/mo/m?kw=%s&lm=&pn=0'%self.HeadURL
        GetFirstPage = requests.get(FirstPageUrl,headers = Header)
        GetFirstPage.encoding = 'utf-8'
        #print GetFirstPage.text
        di = u'第'
        self.PageNumber = re.findall(r'%s1\/(\d*)'%di,GetFirstPage.text)[0]
        self.TieziList = re.findall(r'class\=\"i.{0,3}\"\>\<a.href\=\"(.*?kz=\d*)',GetFirstPage.text)

#帖子信息类
class TieziInfo(object):
    def __init__(self,TieziUrl):
        self.TieziUrl = TieziUrl

    def GetTieziInfoFun(self):
        GetTieziText = requests.get(self.TieziUrl,headers = Header).text
        print GetTieziText
        self.Tiezititle = re.findall(r'\<\/style\>\<title\>(.*?)\<\/title\>',GetTieziText)[0]
        #di = u'第'
        self.TieziPageNumber = int(re.findall(r'%s1\/(\d*)'%di,GetTieziText)[0])
        #lou = u'楼'
        #self.TieziZhuti = re.findall(r'div class\=\"i\"\>1%s\. (.*?)\<br\/\>\<br\/\>\<span class\=\"g\"\>'%lou,GetTieziText)[0]
        #self.TieziHuifuText = re.findall(r'div class\=\"i\"\>1%s\. (.*?)form action\=\"submit\"'%lou,GetTieziText,re.S)[0]
        #self.TieziHuifu = re.findall(r'div class\=\"i\"\>(\d*)%s\. (.*?)\<br.*?href\=\".*?\"\>(.*?)\<\/a.*?\<a href\=\"(flr.*?)\"'%lou,self.TieziHuifuText)

    def GetTieziHuifulist(self,Huililist):
        #for TZi in range(0,self.TieziPageNumber*10,10):
            #self.TieziUrllist = self.TieziUrl+'&pn=%s'%TZi
        #print self.TieziUrllist
        GetTieziTextAll = requests.get(Huililist,headers = Header).text
        print GetTieziTextAll
        #self.TieziZhuti = re.findall(r'div class\=\"i\"\>1%s\. (.*?)\<br\/\>\<br\/\>\<span class\=\"g\"\>'%lou,GetTieziTextAll)[0]
        self.TieziHuifuText = re.findall(r'div class\=\"i\"\>1%s\. (.*?)form action\=\"submit\"'%lou,GetTieziTextAll,re.S)[0]
        #print self.TieziHuifuText
        self.TieziHuifu = re.findall(r'div class\=\"i\"\>(\d*)%s\. (.*?)\<br.*?href\=\".*?\"\>(.*?)\<\/a.*?\<a href\=\"(flr.*?)\"'%lou,self.TieziHuifuText)







tieba = TieBaInfo('%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6')
tieba.GetFirstPageFun()
print tieba.PageNumber
for tz in tieba.TieziList:
    TieziUrl = 'http://tieba.baidu.com'+tz
    tiezi = TieziInfo(TieziUrl)
    tiezi.GetTieziInfoFun()
    print tiezi.TieziPageNumber
    for TZi in range(0,tiezi.TieziPageNumber*10,10):
        #tiezi = TieziInfo(TieziUrl)
        TiezilistUrl = TieziUrl+'&pn=%s'%TZi
        tiezi.GetTieziHuifulist(TiezilistUrl)
        for hf in tiezi.TieziHuifu:
            print hf


        raw_input()
