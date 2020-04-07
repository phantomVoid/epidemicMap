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


url = 'https://masiro.moe/forum.php?mod=viewthread&tid=13763&extra=page%3D1'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

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
    img = html.xpath("//td[@id='postmessage_110311']/*")
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