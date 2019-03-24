# coding: utf-8
from bs4 import BeautifulSoup
import re
import urllib.parse
class HtmlParser(object):
    
    def _get_new_urls(self, page_url, soup):
        new_urls = set();
        links = soup.find_all('a', class_="contentpile__content__wrapper__item__info");
        for link in links:
            new_url = link.find('a')['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
    
    def _get_new_data(self, page_url, soup, type):
        res_data = {} # 定义字典
        res_data['url'] = page_url #收集地址
        res_data['type'] = type #收集类型
        li_node = soup.find('div', class_='summary-plane__info').find('li')
        res_data['name'] = soup.find('div', class_='summary-plane').find('h3').get_text() #收集职位名称
        res_data['public_time'] = ''; #收集发布时间
        res_data['address'] = li_node[0].find('a').get_text(); #收集公司地址
        res_data['salary'] = soup.find('div', clsss_='summary-plane__left').find('span').get_text(); #收集薪资
        res_data['company'] = soup.find('div', class_='company').find('a').get_text()# 收集公司
        res_data['experience'] = li_node[1].get_text();  #收集经验要求
        res_data['education'] = li_node[2].get_text(); # 收集学历要求
        des_node = soup.find('div', class_='describtion__detail-content').find_all('p');
        res_data['duty'] = des_node.get_text() #收集职位描述

    def parse(self, page_url, page_content, type):
        if page_url is None or page_content is None:
            return
        soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8') #利用BeautifulSoup，格式化html源码
        new_data = self._get_new_data(page_url, soup, type) # 调用分析方法获取数据
        return new_data

    # 分析搜索页数据，获取总页数和详细职位地址
    def parse_search_page(self, page_content):
        if page_content is None:
            return
        new_urls = set();
        soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8') #利用BeautifulSoup，格式化html源码
        div_nodes = soup.find('div', class_='contentpile__content__wrapper__item clearfix').find_all('a'); # 职位链接节点
        for node in div_nodes: # 循环链接节点
            new_url = node.find['href'] # 获取连接
            new_urls.add(new_url)
        soupager__index_nodes = soup.find('div', class_='soupager').find_all('span',class_='soupager__index')  #页面总页数节点
        total = soupager__index_nodes[len(soupager__index_nodes) - 2].get_text(); #获取总页数
        return int(total), new_urls