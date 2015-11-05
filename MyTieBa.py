# -*- coding:gbk -*-

import requests
import re

#获取首页
Header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate'
}
FirstPageUrl = 'http://tieba.baidu.com/mo/m?kw=%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6&lm=&pn=0'
GetFirstPage = requests.get(FirstPageUrl,headers = Header).text


