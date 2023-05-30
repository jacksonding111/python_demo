import requests
from lxml import etree

index_url = 'https://tieba.baidu.com/p/5475267611'
# index_url = input('请输入需要下载图片的地址：')

response = requests.get(index_url).text
# print(response)

selector = etree.HTML(response)

image_urls = selector.xpath('//img[@class="BDE_Image"]/@src')

print(image_urls)
#
# offset = 0
# for image_url in image_urls:
#     image_content = requests.get(image_url).content
#     with open('{}.jpg'.format(offset), 'wb') as f:
#         f.write(image_content)
#     offset += 1
# if offset == 0:
#     print('未抓取到有效图片信息')