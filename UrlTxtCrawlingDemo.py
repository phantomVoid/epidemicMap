import requests
from lxml import etree
import requests
import time
import sys
import os
import queue
import json
from bs4 import BeautifulSoup

q = queue.Queue()
# 首先我们写好抓取网页的函数
def get_content(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        content = r.text
        return content
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return " ERROR "

def deepPraseContents(content):
    ret = ""
    try:
        p_content = content.contents[0]
        deepPraseContents(p_content)
    except:
        ret = p_content
        if ret is None:
            ret = " "
        else:
            if str(p_content).find("<br/>") == 0:
                ret = str(p_content).replace("<br/>","")
        return str(ret)
    return str(ret)


# 解析内容
def praseContent(content):
    soup = BeautifulSoup(content,'html.parser')
    pp = soup.find("input", {'class': 'mousetrap'})
    chapter = pp.attrs['value']

    p = soup.find_all("p")
    print(str(chapter))
    for cur_p in p:
        contents = deepPraseContents(cur_p)
        save(chapter, contents)

# 保存数据到txt
def save(chapter, content):
    filename = "books\\"+chapter+".txt"
    f =open(filename, "a+",encoding='utf-8')
    # f.write("".join(chapter)+'\n')
    f.write("".join(content.split())+'\n')
    f.close


url = 'https://www.myfreeblack.com/force-mom-videos/p/2'
headers = {
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    ':authority': 'www.myfreeblack.com',
    ':method': 'GET',
    ':path': '/force%20mom-videos?',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '__cfduid=d3e33006d842f6d1015c486794319cefa1584292171; _ga=GA1.2.1666332073.1584292175; cf_clearance=4b52fec6d0ae856a2cfe977c1a73c141e3dd3e0b-1584876707-0-150; _gid=GA1.2.1421771727.1584876712; _gat_gtag_UA_111579826_2=1; bul_pageCounterjl2n0ga4=31',
    'referer': 'https://www.myfreeblack.com/force%20mom-videos?',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

def get_urls(cur_page):
    return url

def getUrls():
    retUrl = ""
    cur_url = get_urls(url)
    response = requests.get(cur_url)
    data = response.content.decode('utf-8')
    html = etree.HTML(data)
    # img = html.xpath('//a[@*]/@href')
    # img = html.xpath("//td[@id='postmessage_110311']/a/@href")
    img = html.xpath("//img[@class='thumb']/*")
    for i in img:
        try:
            tag = i.tag
            tail = i.tail
            href = i.attrib

            if len(tail) > 5:
                print(tail)
            if len(str(href)) > 20:
                a = str(href)
                href = str(a.replace("'", '').replace(",",":")).split(":")[1]+":"+str(a.replace("'", '').replace(",",":")).split(":")[2]
                if href.find("shimo") >= 0:
                    retUrl = href
                    q.put(retUrl)
                    content = get_content(q.get())
                    praseContent(content)
        except Exception as e:
            print(e)
            continue
    return retUrl

# 主程序
def main():
    start_time = time.time()
    getUrls()
    end_time = time.time()
    project_time = end_time - start_time
    print('程序用时', project_time)

if __name__ == '__main__':
    main()