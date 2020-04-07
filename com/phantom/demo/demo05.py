import requests
from lxml import etree

url = 'https://se.haodd90.com/html/'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def get_urls(cur_page):
    ret_url = url + '125018.html'
    if cur_page > 1:
        ret_url = url + '%d.html' % cur_page
    else:
        ret_url = url + '125018.html'
    print("ret_url: >>> " + ret_url)
    return ret_url

cur_page = 125031
end_page = 148935

while int(end_page) > int(cur_page):
# for ii in (cur_page,end_page):
    cur_item = 1
    cur_url = get_urls(cur_page)
    response = requests.get(cur_url)
    data = response.content.decode('utf-8')
    html = etree.HTML(data)
    img = html.xpath('//img[@*]/@src')
    for i in img:
        try:
            res = requests.get(i, headers=headers)
            img_data = res.content  # 只能转换为字节流才能下载图片
            # with open ('/Users/hspcadmin/{}.jpg'.format(a),'wb') as f:
            path = 'demo05-pics'
            string = str(cur_page) + '-' + str(cur_item) + '.jpg'
            with open(path + '\\' +string, 'ab') as f:
                f.write(img_data)
                print('第%s张图片已下载完成' % string)
                cur_item += 1
        except Exception as e:
            print(e)
            continue
    cur_page += 1