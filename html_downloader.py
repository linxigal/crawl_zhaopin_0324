 # coding: utf-8
import urllib.request, urllib.error, urllib.parse
from urllib.parse import urlencode
class HtmlDownloader(object):
    
    # 下载页面源码方法
    def download_html(self, url):
        if url is None:
            return None
        resp = urllib.request.urlopen(url) #打开地址链接，获取响应报文
        if resp.getcode() != 200:
            return None
        return resp.read()  # 读取响应报文