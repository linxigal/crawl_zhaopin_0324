# coding: utf-8
from bs4 import BeautifulSoup
import re
import urllib.parse
class HtmlParser(object):
    
    def _get_new_urls(self, page_url, soup):
        new_urls = set();
        links = soup.find_all('a', class_="e");
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
    
    def _get_new_data(self, page_url, soup, type):
        res_data = {}   # 定义字典
        res_data['url'] = page_url  #收集地址
        jt_node = soup.find('div', class_='jt')
        res_data['type'] = type #收集类型
        res_data['name'] = jt_node.find('p').get_text(); #收集职位名称
        res_data['public_time'] = jt_node.find('span').get_text(); #收集发布时间
        res_data['address'] = jt_node.find('em').get_text() #收集公司地址
        res_data['salary']  = soup.find('p', class_='jp').get_text() #收集薪资
        res_data['experience'] = ''
        res_data['education'] = ''
        jd_node = soup.find('div', class_='jd')
        s_n_node = jd_node.find('span', class_='s_n')
        s_x_node = jd_node.find('span', class_='s_x')
        if s_n_node is not None:
            res_data['experience'] = s_n_node.get_text()    #收集经验要求
        if s_x_node is not None:
            res_data['education'] = s_x_node.get_text() # 收集学历要求
        res_data['company']  = soup.find('p', class_='c_444').get_text()    # 收集公司
        ain_p_nodes = soup.find('div', class_='ain').find_all('p');
        duty = '';
        requirement = ''
#         flag = 0;
        for node in ain_p_nodes:
            text = node.get_text();
            if text is None or text == '<br>':
                 continue;
            duty = duty + text
            
#             if '任职' in text.encode('utf-8'):
#                 flag = 1;
#             if '公司' in text.encode('utf-8'):
#                 flag = 2;
#             if flag == 0 and text != '<br>':
#                 duty = duty + text
#             elif flag == 1 and text != '<br>':
#                 requirement = requirement + text
        res_data['duty']  = duty #收集岗位职责
#         res_data['requirement']  = requirement
        return res_data;
        
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
        links = soup.find('div', class_='items').find_all('a'); # 职位链接节点
        for link in links: # 循环链接节点
            new_url = link['href']  # 获取连接
            new_urls.add(new_url)
        option_nodes = soup.find('div', class_='paging').find('select') .find_all('option') #页面总页数节点
        total = option_nodes[len(option_nodes) - 1].get_text(); #获取总页数
        return int(total), new_urls
        
        
    