#!/usr/bin/env python
# -*- coding: utf-8 -*-
#         Time:  2021/11/10 19:27
#       Author:  曹忠伟
#         File:  get_info.py
#     Software:  PyCharm
#  explanation:  获取人人都是产品经理文章数据

# 导入包
import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt

# 全局变量
data_list = []
web_url = "http://www.woshipm.com/category/pd/page/"
save_path = "C:/Users/18875/Desktop/编程/Python/PM/人人都是产品经理.xls"

# 正则表达式
find_title = re.compile(r'<a aria-label="(.*?)"')

find_link = re.compile(r'<a aria-label=".*" href="(.*?)"')

find_brief = re.compile(r'itemprop="about">(.*?)</div>', re.S)

find_author = re.compile(r'<a class="ui-captionStrong" href=".*" target="_blank">(.*?)</a>', re.S)

find_author_home = re.compile(r'<a class="ui-captionStrong" href="(.*?)" target="_blank">.*</a>', re.S)

find_page_views = re.compile(r'<div class="meta--sup__right">.*(\d*) 浏览', re.S)

find_time = re.compile(r'<time itemprop="datePublished">(.*?)</time>', re.S)


def url_data(url):
    """获取单个url数据"""

    # 代理服务器和请求数据
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/92.0.4484.7 Safari/537.36"
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url=url, headers=headers)

    # 请求数据
    url_html = urllib.request.urlopen(req)

    return url_html


def web_data(url):
    """获取所有数据"""

    for i in range(1, 20):

        # 调用获取页面函数的次数
        current_url = url + str(i)

        # 获取网页数据
        print("正在获取第%d页数据" % i)
        url_data(current_url)

        # 保存获取的网页源码到内存
        url_html = url_data(current_url)

        # 逐一解析网页数据
        soup = BeautifulSoup(url_html, "html.parser")

        body = soup.body

        for item in body.find_all('div', class_="content"):
            # 测试查看信息
            # print(item)

            item = str(item)
            data = []

            title = re.findall(find_title, item)
            data.extend(title)

            link = re.findall(find_link, item)
            data.extend(link)

            brief = re.findall(find_brief, item)
            data.extend(brief)

            author = re.findall(find_author, item)
            data.extend(author)

            author_home = re.findall(find_author_home, item)
            data.extend(author_home)

            page_views = re.findall(find_page_views, item)
            data.extend(page_views)

            time = re.findall(find_time, item)
            data.extend(time)

            data_list.append(data)

            # print(data_list)

    # 使用删除空列表方法
    nested_check(data_list)

    print(data_list)

    return data_list


def save_data(path):
    """储存处理后的数据到excel表"""

    # 创建表格
    book = xlwt.Workbook(encoding="utf-8")  # 工作簿
    sheet = book.add_sheet("info")  # 创建工作表

    # 准备数据
    title = ["标题", "链接", "摘要", "作者", "作者主页", "浏览量", "发表时间"]

    # 写入数据
    for i in range(0, 7):
        sheet.write(0, i, title[i])

    for i in range(0, 220):
        print("正在写入第%d条" % (i+1))

        data = data_list[i]

        for j in range(0, 7):
            sheet.write(i+1, j, data[j])

    print("数据写入成功")

    # 保存表格
    book.save(path)
    print("保存成功")


def remove_nested_list(list0):
    """删除空列表"""
    for index, value in enumerate(reversed(list0)):
        if isinstance(value, list) and value != []:
            remove_nested_list(value)
        elif isinstance(value, list) and len(value) == 0:
            list0.remove(value)


def nested_check(alist):
    """删除空列表方法2"""
    for item in alist[:]:
        if item == []:
            alist.remove(item)
        elif isinstance(item, list):
            nested_check(item)

# 调用函数
if __name__ == '__main__':
    web_data(web_url)
    save_data(save_path)
