# coding: utf-8
import url_manager
import html_downloader
import html_parser
import html_parser_zhaopin
import outputer
from urllib.parse import quote
import sys

class SpiderMian(object):
    
    # 实例化爬虫模块
    def __init__(self):
        self.urls = url_manager.UrlManager() # url管理器
        self.downloder = html_downloader.HtmlDownloader() # 网页下载器
        self.parser = html_parser.HtmlParser() # 51JOB网页解析器
        self.html_parser_zhaopin = html_parser_zhaopin.HtmlParser() # 招聘网页解析器
        self.outputer = outputer.Outputer() # 结果输出
    
    def craw(self, net_info):
        _page_total = 1;
        currentPage = 1;
        count = 1;
        parser = self.parser
        craw_type = net_info['type'] + '-' + net_info['keyword']    #拼接抓取分类
        if net_info['type'] == '51job' :    # 如果网站类型是51job
            search_url = net_info['url'] + '&pageno=' + str(currentPage) + '&keyword=' + net_info['keyword']    # 拼接首页查询地址
            html_content = self.downloder.download_html(search_url) # 下载首页查询页面源码
            page_total, new_urls = self.parser.parse_search_page(html_content) # 分析首页查询页面，获取分页总数和职位详细的地址
            self.urls.add_new_urls(new_urls)    #把职位详细的地址加入到url管理器
            _page_total = page_total
            parser = self.parser
        elif net_info['type'] == 'zhaopin' : # 如果网站类型是zhaopin
            search_url = net_info['url'] + '&p=' + str(currentPage) + '&kw=' + net_info['keyword'] # 拼接首页查询地址
            print(search_url);
            html_content = self.downloder.download_html(search_url) # 下载首页查询页面源码
            page_total, new_urls = self.html_parser_zhaopin.parse_search_page(html_content) # 分析首页查询页面，获取分页总数和职位详细的地址
            self.urls.add_new_urls(new_urls)  #把职位详细的地址加入到url管理器
            _page_total = page_total
            parser = self.html_parser_zhaopin
        # while循环，遍历新的url，解析网页获取数据
        while self.urls.has_new_url():
            try:
                urls_len, new_url = self.urls.get_new_url() # 从url管理器中，获取未抓取的url
                print("carwing for: ", count, new_url)
                html_content = self.downloder.download_html(new_url) # 下载详情页源码
                new_data = parser.parse(new_url, html_content, craw_type) # 解析网页，获取数据
                self.outputer.collect_data(new_data)    # 收集数据
                self.outputer.save_data_todb(new_data) # 保存到数据库
                count = count + 1;
                if count > 40000:  # 如果爬到400条数据，终止程序。
                    break;
                if urls_len == 0 and currentPage <= _page_total:    # 如果url管理器没有新的地址，并且当前查询页面的页数小于总页数，抓取当前页，获取新的地址
                    currentPage = currentPage + 1;
                    if net_info['type'] == '51job' :
                        search_url = net_info['url'] + '&pageno=' + str(currentPage) + '&keyword=' + net_info['keyword'] # 拼接首页查询地址
                        html_content = self.downloder.download_html(search_url) # 下载首页查询页面源码
                        page_total, new_urls = self.parser.parse_search_page(html_content) # 分析首页查询页面，获取分页总数和职位详细的地址
                        self.urls.add_new_urls(new_urls)  #把职位详细的地址加入到url管理器
                    elif net_info['type'] == 'zhaopin' :
                        search_url = net_info['url'] + '&p=' + str(currentPage) + '&kw=' + net_info['keyword'] # 拼接首页查询地址
                        #print search_url
                        html_content2 = self.downloder.download_html(search_url) # 下载首页查询页面源码
                        page_total, new_urls = self.html_parser_zhaopin.parse_search_page(html_content2) # 分析首页查询页面，获取分页总数和职位详细的地址
                        _page_total = page_total
                        self.urls.add_new_urls(new_urls) #把职位详细的地址加入到url管理器
            except Exception as e:
                print('抓取失败！', e)
        self.outputer.output_html() # 把数据输出到html文件
        self.outputer.close_db()    # 关闭数据库
         #self.outputer.save_all_data_todb()

if __name__=="__main__":
    net_info1 = {
         'url': 'https://m.51job.com/search/joblist.php?jobarea=000000&keywordtype=2',
         'keyword': '知识产权',
         'type': '51job'
     }
    net_info = {
        'url': 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国', # https://sou.zhaopin.com/?pageSize=60&jl=%E5%85%A8%E5%9B%BD&kt=3
        'keyword': '知识产权',#'keyword': '知识产权',
        'type': 'zhaopin'
    }
    
    
    obj_spider = SpiderMian()   # 实例化爬虫
    obj_spider.craw(net_info1)   # 调用爬虫抓取方法
    #obj_spider.craw(net_info)   # 调用爬虫抓取方法
    #craw_type = net_info['type'] + '-' + net_info['keyword']
    #obj_spider.test('http://jobs.zhaopin.com/199566025253994.htm', craw_type)

    
    
    
    
    
    
    
    
    
    
