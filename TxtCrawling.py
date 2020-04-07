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

# 主程序
def main():
    start_time = time.time()
    q.put(url)
    # 如果队列为空，则继续
    while not q.empty():
        content = get_content(q.get())
        praseContent(content)
    end_time = time.time()
    project_time = end_time - start_time
    print('程序用时', project_time)

# 接口地址
url = 'https://shimo.im/docs/hqKxwrRJG3ThrcH3/read'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

if __name__ == '__main__':
    main()