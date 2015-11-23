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
shuaxin = u'刷新'
stopnum = 3

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
        #di = u'第'
        self.PageNumber = re.findall(r'%s1\/(\d*)'%di,GetFirstPage.text)[0]
        #self.TieziList = re.findall(r'class\=\"i.{0,3}\"\>\<a.href\=\"(.*?kz=\d*)',GetFirstPage.text)

    def GetPageListFun(self,Allurl):
        #for LN in range(0,stopnum,20):
            #PageListUrl = 'http://tieba.baidu.com/mo/m?kw=%s&lm=&pn='%self.HeadURL+str(LN)
        GetPageList = requests.get(Allurl,headers = Header)
        self.TieziListAll = re.findall(r'class\=\"i.{0,3}\"\>\<a.href\=\"(.{70,90}kz=\d+)',GetPageList.text)
        print self.TieziListAll



#帖子信息类
class TieziInfo(object):
    def __init__(self,TieziUrl):
        self.TieziUrl = TieziUrl

    def GetTieziInfoFun(self):
        GetTieziText = requests.get(self.TieziUrl,headers = Header).text
        #print GetTieziText
        self.Tiezititle = re.findall(r'\<\/style\>\<title\>(.*?)\<\/title\>',GetTieziText)[0]
        try:
            self.TieziTime = re.findall(r'div class\=\"i\"\>1%s\..*?\<span class\=\"b\"\>(.*?)(\d{1,2}\:\d{1,2})\<\/span\>'%lou,GetTieziText)[0]
        except:
            self.TieziTime = (u'0',u'0')


        try:
            self.TieziPageNumber = int(re.findall(r'%s1\/(\d*)'%di,GetTieziText)[0])
        except:
            self.TieziPageNumber = 1


        self.TieziZhuti = re.findall(r'div class\=\"i\"\>1%s\. (.*?)\<br\/\>\<br\/\>\<span class\=\"g\"\>'%lou,GetTieziText)
        #self.TieziHuifuText = re.findall(r'div class\=\"i\"\>1%s\. (.*?)form action\=\"submit\"'%lou,GetTieziText,re.S)[0]
        #self.TieziHuifu = re.findall(r'div class\=\"i\"\>(\d*)%s\. (.*?)\<br.*?href\=\".*?\"\>(.*?)\<\/a.*?\<a href\=\"(flr.*?)\"'%lou,self.TieziHuifuText)

    def GetTieziHuifulist(self,Huililist):

        GetTieziTextAll = requests.get(Huililist,headers = Header).text
        #print GetTieziTextAll
        #self.TieziZhuti = re.findall(r'div class\=\"i\"\>1%s\. (.*?)\<br\/\>\<br\/\>\<span class\=\"g\"\>'%lou,GetTieziTextAll)[0] #只能在第一页回复中使用的帖子主题获取
        #self.TieziTime = re.findall(r'div class\=\"i\"\>1%s\..*?\<span class\=\"b\"\>(\d{1,2}\-\d{1,2}) \d{1,2}\:\d{1,2}\<'%lou,GetTieziTextAll)[0]
        self.TieziHuifuText = re.findall(r'%s\<\/a\>\<\/div\>\<div\ class\=\"d\"\>(.*?)form action\=\"submit\"'%shuaxin,GetTieziTextAll,re.S)[0]
        #self.TieziHuifuText = re.findall(r'div class\=\"i\"\>1%s\. (.*?)form action\=\"submit\"'%lou,GetTieziTextAll,re.S)[0] #只能在第一页用的帖子主体内容获取
        #print self.TieziHuifuText
        self.TieziHuifu = re.findall(r'div class\=\"i\"\>(\d*)%s\. (.*?)\<br.*?href\=\".*?\"\>(.*?)\<\/a.*?span class\=\"b\"\>(\d.*?\d)\<.*?\<a href\=\"(flr.*?)\"'%lou,self.TieziHuifuText)



tieba = TieBaInfo('%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6')
tieba.GetFirstPageFun()
print tieba.PageNumber
HeadUrl = tieba.HeadURL
for LN in range(0,stopnum*20,20):
    print "***************************************************************************"
    PageListUrl = 'http://tieba.baidu.com/mo/m?kw=%s&lm=&pn='%HeadUrl+str(LN)
    tieba.GetPageListFun(PageListUrl)


    for tz in tieba.TieziListAll:
        TieziUrl = 'http://tieba.baidu.com'+tz
        print TieziUrl
        tiezi = TieziInfo(TieziUrl)
        tiezi.GetTieziInfoFun()
        print tiezi.TieziPageNumber
        print tiezi.TieziTime
        if tiezi.TieziTime[0] == None:
            pass
        else:

            if re.match(r'11\-\d{1,2}',tiezi.TieziTime[0]):
                for TZi in range(0,tiezi.TieziPageNumber*10,10):

                    TiezilistUrl = TieziUrl+'&pn=%s'%TZi
                    tiezi.GetTieziHuifulist(TiezilistUrl)
                    #print tiezi.TieziTime
                #if re.match(r'11\-\d{1,2}',tiezi.TieziTime):
                    for hf in tiezi.TieziHuifu:
                        print hf[0]
                        print hf[1]
                        print hf[2]
                        print hf[3]


        #raw_input()
