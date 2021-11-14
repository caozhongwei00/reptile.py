"""
douban
"""

from douban_reptile import module

# 数据准备
web_url = "http://movie.douban.com/top250?start="
save_path = "豆瓣电影Top250_4.xls"

# 主函数
if __name__ == '__main__':

    # 获取网页数据,解析网页数据
    module.web_data(web_url)
    print("成功获取数据、并完成解析，即将进行读写任务。")

    # 保存网页数据
    module.save_data(save_path)
    print("已保存，请查看%s工作表。" % save_path)

    print("爬虫任务over")
