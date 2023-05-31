import json
import os
import sys

import requests
import shutil
import time

if __name__ == '__main__':
    # UA伪装:将访问对象伪装为浏览器
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 此条少了就会"Forbid spider access"
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        # 此条少了就会"Forbid spider access"
        'Upgrade-Insecure-Requests': '1'
    }
    # 爬虫主体
    keyword = input("请输入要搜索的图片关键字：")
    current_path = os.path.dirname(__file__)  # 获取当前目录
    try:
        os.mkdir(current_path + '\\' + keyword)  # 在当前路径下创建新文件夹
        print("文件夹已创建成功")
    except FileExistsError as e:
        print(f'当前发生的错误为{e}')
        print("正在删除当前同名文件夹...")
        time.sleep(1)
        file_path = current_path + '\\' + keyword
        shutil.rmtree(file_path)
        os.mkdir(file_path)
        print("新文件夹已创建成功")
    for num in range(0, 3):  # 一次请求返回30张图，此处循环3次，爬取 90 张图片
        # 将输入的关键字嵌进发送请求的url中
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&z=&ic=0&word=' \
              + keyword + '&face=0&istype=2&nc=1&pn=' + str(num * 30) + '&rn=30'
        response = requests.get(url=url, headers=headers).json()
        for index in range(len(response['data']) - 1):
            print(response['data'][index]['thumbURL'])
            print(num * 30 + index)
            # 从拿到的网址里下载图片
            img_data = requests.get(response['data'][index]['thumbURL']).content
            # 存图
            with open(current_path + '\\' + keyword + '\\' + str(num * 30 + index) + '.jpg', 'wb', ) as fp:
                fp.write(img_data)
