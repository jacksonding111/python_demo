import re
import requests
import time
from urllib import parse
import os
from fake_useragent import UserAgent  # 随机生成一个user-agent
import chardet


class Picture:

    def __init__(self):
        self.name_ = input('请输入关键字：')
        self.name = parse.quote(self.name_)
        self.times = str(int(time.time() * 1000))
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8032920601831512061&ipn=rj&ct' \
                   '=201326592&is=&fp=result&fr=&word={}&cg=star&queryWord={' \
                   '}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width' \
                   '=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=1e&{}='
        self.headers = {'User-Agent': UserAgent().random}

    # 请求30张图片的链接
    def get_one_html(self, url, pn):
        response = requests.get(url=url.format(self.name, self.name, pn, self.times), headers=self.headers).content.decode('utf-8')
        return response

    # 解析含30张图片的html内容
    def parse_html(self, regex, html):
        encode_type = chardet.detect(html)
        html = html.decode(encode_type['encoding'])
        content = regex.findall(html)
        return content

    # 主函数
    def run(self):
        # 判断该路径下是否存在同名文件夹 如果没有则创建 有就不执行If下的创建
        if not os.path.exists('./{}/'.format(self.name_)):
            os.mkdir('./{}/'.format(self.name_))
        response = self.get_one_html(self.url, 0)
        regex1 = re.compile('"displayNum":(.*?),')
        num = self.parse_html(regex1, response)[0]  # 获取总的照片数量
        print('该关键字下一共有{}张照片'.format(num))

        # 判断总数能不能整除30
        if int(num) % 30 == 0:
            pn = int(num) / 30
        else:
            # 总数量除30是因为每个链接有30张照片 +2是因为想range最多取到该数就需要+1
            # 另外的+1是因为该总数除30可能有余数，有余数就需要一个链接 所以要+1
            pn = int(num)

        for i in range(pn):
            resp = self.get_one_html(self.url, i * 30)
            regex2 = re.compile('"middleURL":"(.*?)"')
            urls = self.parse_html(regex2, resp)
            for u in urls:
                content = self.get_one_html(u)
                with open('./{}/{}.jpg'.format(self.name_, u[28:35]), 'wb') as f:
                    f.write(content)
                print('完成一张照片')


if __name__ == '__main__':
    spider = Picture()
    spider.run()
