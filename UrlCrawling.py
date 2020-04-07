import requests
from lxml import etree

url = 'https://masiro.moe/forum.php?mod=viewthread&tid=13763&extra=page%3D1'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def get_urls(cur_page):
    return url

cur_page = 125023
end_page = 148935

for ii in (cur_page,end_page):
    cur_item = 1
    cur_url = get_urls(cur_page)
    response = requests.get(cur_url)
    data = response.content.decode('utf-8')
    html = etree.HTML(data)
    # img = html.xpath('//a[@*]/@href')
    # img = html.xpath("//td[@id='postmessage_110311']/a/*")
    img = html.xpath("//td[@id='postmessage_110311']/*")
    for i in img:
        try:
            tag = i.tag
            tail = i.tail
            href = i.attrib
            # if len(tail) > 5:
            print(tail)
            # if len(str(href)) > 20:
            a = str(href)
            href = str(a.replace("'", '').replace(",",":")).split(":")[1]+":"+str(a.replace("'", '').replace(",",":")).split(":")[2]
            if href is None:
                href = ""
            else:
                if href == None:
                    href = ""
                else:
                    print(href)
        except Exception as e:
            # print(e)
            continue