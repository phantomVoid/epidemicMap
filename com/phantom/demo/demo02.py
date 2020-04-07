import requests
from lxml import etree

# todo 爬取贴吧图片

# url = 'https://tieba.baidu.com/p/5815297430'
url = 'https://tieba.baidu.com/p/6302871230'
# url = 'https://tieba.baidu.com/p/6469095166'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
response = requests.get(url)
data = response.content.decode('utf-8')

# 解析
html = etree.HTML(data)
img = html.xpath('//img[@class="BDE_Image"]/@src')
a = 1
for i in img:
    res = requests.get(i, headers=headers)
    img_data = res.content  # 只能转换为字节流才能下载图片
    # with open ('/Users/hspcadmin/{}.jpg'.format(a),'wb') as f:
    path = 'demo02-pics'
    with open(path + '\\%d.jpg' % a, 'ab') as f:
        # with open ('/Users/hspcadmin/{}.jpg'.format(a)) as f:
        f.write(img_data)
        print('第%d张图片已下载完成' % a)
        a += 1
