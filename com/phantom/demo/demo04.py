import requests
from lxml import etree

url = 'https://www.myfreeblack.com/force%20mom-videos?'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def get_onepage_urls(cur_page):
    ret_url = url + '1.html'
    if cur_page > 1:
        ret_url = url + '1-%d.html' % cur_page
    else:
        ret_url = url + '1.html'
    print("ret_url: >>> " + ret_url)
    return ret_url


for ii in range(page_num):
    cur_url = get_onepage_urls(cur_page)
    response = requests.get(cur_url)
    data = response.content.decode('utf-8')
    html = etree.HTML(data)
    img = html.xpath('//img[@*]/@src')
    for i in img:
        res = requests.get(i, headers=headers)
        img_data = res.content  # 只能转换为字节流才能下载图片
        path = 'demo04-pics'
        string = str(cur_page) + '-' + str(cur_item) + '.jpg'
        with open(path + '\\' +string, 'ab') as f:
            f.write(img_data)
            print('第%s张图片已下载完成' % string)
            cur_item += 1