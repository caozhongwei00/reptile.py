import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt

# 全局变量
data_list = []

# 创建正则表达式对象
# 影片链接
find_link = re.compile(r'<a href="(.*?)">')

# 影片的图片
find_img = re.compile(r'<img.*src="(.*?)"', re.S)     # re.S,让换行符包含在字符串中

# 影片的中文片名
# <span class="title">肖申克的救赎</span>
find_chi_name = re.compile(r'<span class="title">(.*)</span>')

# 影片的主题
# <span class="inq">希望让人自由。</span>
find_theme = re.compile(r'<span class="inq">(.*)</span>')

# 影片的评价人数
# <span>2479345人评价</span>
find_num = re.compile(r'<span>(\d*)人评价</span>')

def url_data(web_url):
    """获取1个指定的url数据"""

    # 代理服务器和请求数据
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4484.7 Safari/537.36"
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url=web_url, headers=headers)

    # 请求数据
    url_html = urllib.request.urlopen(req)

    return url_html


def web_data(web_url):
    """循环，获取一组特定url的数据"""

    for i in range(0, 10):
        # 调用获取页面函数的次数：10次
        current_url = web_url + str(i*25)

        # 保存获取的网页源码到内存
        url_html = url_data(current_url)

        # 逐一解析网页数据
        soup = BeautifulSoup(url_html, "html.parser")

        for item in soup.find_all('div', class_="item"):
            # print(item) # 测试查看信息
            data = []
            item = str(item)

            # 从解析后的网页数据中，提取指定内容
            link = re.findall(find_link, item)
            data.append(link)

            img_link = re.findall(find_img, item)
            data.append(img_link)

            chi_name = re.findall(find_chi_name, item)[0]
            data.append(chi_name)

            theme = re.findall(find_theme, item)
            data.append(theme)

            num = re.findall(find_num, item)
            data.append(num)

            data_list.append(data)

    # print(data_list)

    return data_list


def save_data(save_path):
    """储存处理后的数据到excel表"""

    # 创建表格
    book = xlwt.Workbook(encoding="utf-8")  # 工作簿
    sheet = book.add_sheet("movie")  # 创建工作表

    # 准备数据
    title = ["链接", "图片", "中文名", "主题", "评价人数"]

    # 写入数据
    for i in range(0, 5):
        sheet.write(0, i, title[i])

    for i in range(0, 250):
        print("正在写入第%d条" % (i+1))

        data = data_list[i]

        for j in range(0, 5):
            sheet.write(i+1, j, data[j])

    # 保存表格
    book.save(save_path)
