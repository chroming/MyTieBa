# -*- coding:utf-8 -*-


import requests
import re
import MySQLdb
from datetime import date
from multiprocessing import Pool




# 贴吧类
class TieBaInfo(object):
    def __init__(self, URL):
        self.HeadURL = URL

    # 获取首页HTML及本吧帖子总页数
    def GetFirstPageFun(self):

        FirstPageUrl = 'http://tieba.baidu.com/mo/m?kw=%s&lm=&pn=0' % self.HeadURL
        GetFirstPage = requests.get(FirstPageUrl, headers=Header)
        GetFirstPage.encoding = 'utf-8'
        self.PageNumber = re.findall(r'%s1/(\d*)' % di, GetFirstPage.text)[0]

    # 获取前stopnum页数的帖子URL,主题,总回复数
    def GetPageListFun(self, Allurl):
        GetPageList = requests.get(Allurl, headers=Header)
        # 以下正则组匹配内容依次为:URl,主题,回帖数
        self.TieziListAll = re.findall(r'class\=\"i.{0,3}\"\>\<a.href\=\"(.{70,90}kz=\d+)\&.*?\>\d*\.\&\#160\;(.*?)\<\/a\>.*?%s(\d*)'%hui,GetPageList.text)


# 帖子信息类
class TieziInfo(object):
    def __init__(self, TieziUrl):
        self.TieziUrl = TieziUrl

    # 获取帖子标题,时间,回复页数
    def GetTieziInfoFun(self):
        GetTieziText = requests.get(self.TieziUrl, headers=Header).text
        self.Tiezititle = re.findall(r'</style><title>(.*?)</title>', GetTieziText)[0]
        try:
            self.TieziTime = re.findall(r'div class\=\"i\">1%s\..*?<span class=\"b\">(.*?)(\d{1,2}:\d{1,2})?</span>' % lou, GetTieziText)[0]
        except:
            self.TieziTime = (u'0', u'0')

        # 帖子回复页数
        try:
            self.TieziPageNumber = int(re.findall(r'%s1/(\d*)' % di, GetTieziText)[0])
        except:
            self.TieziPageNumber = 1


        self.TieziZhuti = re.findall(r'div class\=\"i\"\>1%s\. (.*?)\<br\/\>\<br\/\>\<span class\=\"g\"\>'%lou,GetTieziText)

    def GetTieziHuifulist(self, Huililist):

        GetTieziTextAll = requests.get(Huililist, headers = Header).text
        self.TieziHuifuText = re.findall(r'%s\<\/a\>\<\/div\>\<div\ class\=\"d\"\>(.*?)form action\=\"submit\"'%shuaxin,GetTieziTextAll,re.S)[0]
        # 以下正则组匹配内容依次为:帖子楼层;帖子内容;回帖ID;回帖时间;回帖链接
        self.TieziHuifu = re.findall(r'div class\=\"i\"\>(\d*)%s\. (.*?)\<br\/\>\<span class\=\"g\".*?href\=\".*?\"\>(.*?)\<\/a.*?span class\=\"b\"\>(\d.*?\d)\<.*?\<a href\=\"(flr.*?)\"'%lou, self.TieziHuifuText)


def GetRealContent(content):
    return re.sub(r'<.*?>', '', content)


def getinfo(stopnum, tieba):
    try:
        tbdb = MySQLdb.connect("localhost", "pub", "password", "tiebadb", charset="utf8")
    except:
        print("数据库连接失败!请检查MySQL是否在运行! ")
        return None

    cursor = tbdb.cursor()
    HeadUrl = tieba.HeadURL
    # 循环获取前stopnum页帖子URL
    for LN in range(0, stopnum*20, 20):
        PageListUrl = 'http://tieba.baidu.com/mo/m?kw=%s&lm=&pn=' % HeadUrl+str(LN)
        tieba.GetPageListFun(PageListUrl)

        # 循环帖子URL获取HTML
        for tz in tieba.TieziListAll:
            TieziUrl = 'http://tieba.baidu.com'+tz[0]
            tiezi = TieziInfo(TieziUrl)
            tiezi.GetTieziInfoFun()
            print tz[0], tz[1], tz[2], tiezi.TieziPageNumber, tiezi.TieziTime[0], tiezi.TieziTime[1]
            if tiezi.TieziTime[0]:
                if len(tiezi.TieziTime[0]) < 6:
                    tzdate = today[0:4] + "-" + tiezi.TieziTime[0]
                else:
                    tzdate = tiezi.TieziTime[0]
            else:
                tzdate = today

            sql = "insert into tiezilist values ('%s','%s','%s','%s','%s','%s')" % (tz[0], tz[1], tz[2], tiezi.TieziPageNumber, tzdate, tiezi.TieziTime[1])

            try:
                cursor.execute(sql)
                tbdb.commit()
            except:
                print("Error")
                tbdb.rollback()

            if tiezi.TieziTime[0] is not None:
                if 1 == 2:
                # 判断帖子时间的代码.暂时不使用
                #if re.match(r'3\-\d{1,2}', tiezi.TieziTime[0]):
                    for TZi in range(0, tiezi.TieziPageNumber*10, 10):

                        TiezilistUrl = TieziUrl+'&pn=%s'%TZi
                        tiezi.GetTieziHuifulist(TiezilistUrl)
                        #print tiezi.TieziHuifu
                        for hf in tiezi.TieziHuifu:
                            realcontent = GetRealContent(hf[1])
                            print hf[0]
                            print realcontent
                            print len(realcontent)
                            print hf[2]
                            print hf[3]
    tbdb.close()


def main():
    #tieba = TieBaInfo('%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6')
    tiebaname = raw_input("请输入贴吧名称: ")
    tieba = TieBaInfo(tiebaname)
    tieba.GetFirstPageFun()
    print("本吧帖子总页数: "+str(tieba.PageNumber))
    try:
        stopnum = int(raw_input("请输入需要抓取的页数,贴子数=页数*20: "))
    except :
        print("页数只能为数字!请重新输入!")
        main()
    finally:
        if stopnum > 200:
            print("页数不能超过200 !请重新输入!")
            main()
        else:
            getinfo(stopnum, tieba)

if __name__ == '__main__':
    Header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }

    di = u'第'
    lou = u'楼'
    shuaxin = u'刷新'
    hui = u'回'
    # 截止页指手机页面的截止页,每页20个帖子
    # stopnum = 10
    today = str(date.today())
    main()
