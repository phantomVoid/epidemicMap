import os
import shutil
import requests
from lxml import etree
import re
import pymysql


url = 'https://www.kylc.com/stats/global/yearly/g_population_total/'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='python',charset='utf8mb4')
cursor = db.cursor()


cur_page = 1959
end_page = 2018

def truncate_table():
    sql = "truncate table population"
    cursor.execute(sql)
    db.commit()
    print(">>> 表数据初始化成功")

def insert_to_mysql(name_str,type_str,value_num,date_str,area_str):
    try:
        sql = "insert into population(name_str,type_str,value_num,date_str,area_str) values ('%s','%s','%s','%s','%s')"%(name_str,type_str,value_num,date_str,area_str)
        cursor.execute(sql)
        db.commit()
        print("成功写入数据库，{%s,%s,%s,%s,%s}"%(name_str,type_str,value_num,date_str,area_str))
    except:
        pass

def get_urls(cur_page):
    ret_url = url + '1959.html'
    if cur_page > 1:
        ret_url = url + '%d.html' % cur_page
    else:
        ret_url = url + '1959.html'
    print("ret_url: >>> " + ret_url)
    return ret_url

# 保存数据到txt
def save(chapter, content):
    filename = './txt/'+chapter+".txt"
    fout = open(filename, 'a+', encoding='UTF-8')
    # filename = chapter
    # f =open(filename, "a+",encoding='utf-8')
    try:
        fout.write(content.strip() + '\n')
        # print(filename+'文件写入成功！')
        # f.write("".join(content.split())+'\n')
    except Exception as e:
        os.mknod(filename)
        fout.write(content.strip() + '\n')
        pass
    fout.close

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

if __name__ == '__main__':
    shutil.rmtree('./txt/')
    os.mkdir('./txt/')
    truncate_table()
    while int(end_page) > int(cur_page):
        # for ii in (cur_page,end_page):
        cur_item = 1
        cur_url = get_urls(cur_page)
        response = requests.get(cur_url)
        data = response.content.decode('utf-8')
        html = etree.HTML(data)
        # img = html.xpath('//img[@*]/@src')
        img = html.xpath('//tbody/tr//td')

        item_text = ''
        line_text = ''

        name_str = ''
        type_str = '总人口'
        value_num = ''
        date_str = cur_page
        area_str = ''

        lo = 0
        ro = 1
        for i in img:
            item_text = i.text
            try:
                lo = lo + 1
                if ro % 40 == 0:
                    ro = ro +1
                else:
                    if lo % 5 == 0:
                        line_text = '%s,%s,%s,%d' % (name_str, type_str, value_num, date_str)
                        lo = 0
                        ro = ro +1
                        # contents = deepPraseContents(line_text)
                        # save(str(cur_page),line_text)
                        insert_to_mysql(name_str, type_str, value_num, date_str, area_str)
                        # print(line_text)
                        line_text = ''
                    else:
                        if lo == 1:
                            if item_text is None or item_text.strip() is None or item_text.isspace():
                                if ro > 42:
                                    lo = lo-1
                                continue
                            else:
                                name_str = item_text
                        if lo == 2:
                            name_str = item_text
                        if lo == 3:
                            area_str = item_text
                        if lo == 4:
                            item_text = re.findall(r'[(](.*?)[)]', item_text)
                            value_num = item_text[0].replace(',','')
            except Exception as e:
                continue
        cur_page += 1
