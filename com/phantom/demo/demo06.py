import requests
from lxml import etree

url = 'http://dzb.hxnews.com/'
year = 2018
month = 1
day = 1
page = 2

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}


def get_urls(year, month, day, page):
    ret_url = url + str(year) + '-%02d/%02d/node_%01d.htm' % (month, day, page)
    print("ret_url: >>> " + ret_url)
    return ret_url

cur_month = 5
end_month = 13

while int(end_month) > int(cur_month):
    cur_day = 24
    end_day = 31
    while int(end_day) > int(cur_day):
        cur_page = 2
        end_page = 12
        try:
            while int(end_page) > int(cur_page):
                cur_url = get_urls(year, cur_month, cur_day, cur_page)
                response = requests.get(cur_url)
                data = response.content.decode('utf-8')
                html = etree.HTML(data)
                img = html.xpath('//img[@*]/@src')
                # for i in img:
                cur_img = str(img[0]).replace('../../', url)
                print("cur_img: >>> ")
                print(cur_img)

                try:
                    res = requests.get(cur_img, headers=headers)
                    img_data = res.content  # 只能转换为字节流才能下载图片
                    # with open ('/Users/hspcadmin/{}.jpg'.format(a),'wb') as f:
                    path = 'demo06-pics'
                    string = str(cur_month) + '-' + str(cur_day) + '-' + str(cur_page) + '.jpg'
                    with open(path + '\\' + string, 'ab') as f:
                        f.write(img_data)
                        print('第%s张图片已下载完成' % string)
                except Exception as e:
                    print("this is page Exception: >>> ")
                    print(e)
                    continue
                cur_page += 1
            cur_day += 1
        except Exception as e:
            print("this is day Exception: >>> ")
            cur_day += 1
            print(cur_day)
            print(e)
            continue
    cur_month += 1
