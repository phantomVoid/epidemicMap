# coding=utf-8
# sinascr.py 输入指定用户ID，爬取这些用户的微博信息和内容
"""
Created on 2018-3-29 @author: goaza123

功能: 爬取新浪微博用户的信息
信息：用户ID 用户名 粉丝数 关注数 微博数 微博内容
网址：http://weibo.com/, http://weibo.cn/无法访问

"""

import time
import re
import os
import sys
import codecs
import shutil
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 先调用无界面浏览器PhantomJS或Firefox
# driver = webdriver.PhantomJS(executable_path="G:\phantomjs-1.9.1-windows\phantomjs.exe")
driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver, 10)

# 全局变量 文件操作读写信息
inforead = codecs.open("SinaWeibo_List.txt", 'r', 'utf-8')
infofile = codecs.open("SinaWeibo_Info.txt", 'a', 'utf-8')


# ********************************************************************************
#                  第一步: 登陆weibo.cn 获取新浪微博的cookie
#        该方法针对weibo.cn有效(明文形式传输数据) weibo.com见学弟设置POST和Header方法
#                LoginWeibo(username, password) 参数用户名 密码
#                             验证码暂停时间手动输入
# ********************************************************************************

def LoginWeibo(username, password):
    try:
        # **********************************************************************
        # 直接访问driver.get("http://weibo.cn/5824697471")会跳转到登陆页面 用户id
        #
        # 用户名<input name="mobile" size="30" value="" type="text"></input>
        # 密码 "password_4903" 中数字会变动,故采用绝对路径方法,否则不能定位到元素
        #
        # 勾选记住登录状态check默认是保留 故注释掉该代码 不保留Cookie 则'expiry'=None
        # **********************************************************************

        # 输入用户名/密码登录
        print
        u'准备登陆Weibo.cn网站...'
        driver.get("https://weibo.com/")
        time.sleep(10)  # 等待页面载入
        elem_user = driver.find_element_by_id('loginname')
        elem_user.clear()
        elem_user.send_keys(username)  # 用户名
        elem_pwd = driver.find_element_by_class_name('password').find_element_by_name('password')
        elem_pwd.clear()
        elem_pwd.send_keys(password)  # 密码
        # elem_rem = driver.find_element_by_id("login_form_savestate")
        # elem_rem.click()             #记住登录状态

        elem_sub = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')
        elem_sub.click()  # 点击登陆
        time.sleep(10)  # 重点: 暂停时间输入验证码
        elem_sub.click()  # 点击登陆

        # 获取Coockie 推荐 http://www.cnblogs.com/fnng/p/3269450.html
        # print driver.current_url
        # print driver.get_cookies()  # 获得cookie信息 dict存储
        # print u'输出Cookie键值对信息:'
        for cookie in driver.get_cookies():
            # print cookie
            for key in cookie:
                print
                key, cookie[key]

        # driver.get_cookies()类型list 仅包含一个元素cookie类型dict
        print
        u'登陆成功...'
        time.sleep(5)
    except Exception as e:
        print
        "Error: ", e


# ********************************************************************************
#                  第二步: 访问个人页面http://weibo.cn/302579176并获取信息
#                                VisitPersonPage()
#        编码常见错误 UnicodeEncodeError: 'ascii' codec can't encode characters
# ********************************************************************************

def VisitPersonPage(user_id):
    try:
        global infofile
        print
        u'准备访问个人网站.....'
        # 原创内容 http://weibo.cn/guangxianliuyan?filter=1&page=2
        driver.get("http://weibo.com/" + user_id + "?profile_ftype=1&is_all=1#_0")

        # **************************************************************************
        # No.1 直接获取 用户昵称 微博数 关注数 粉丝数
        #      str_name.text是unicode编码类型
        # **************************************************************************

        # 用户id
        print
        u'个人详细信息'
        print
        '**********************************************'
        print
        u'用户id: ' + user_id

        # 昵称
        str_name = driver.find_element_by_xpath("//div[@class='pf_username']")
        str_t = str_name.text.split(" ")
        num_name = str_t[0]  # 空格分隔 获取第一个值 "Eastmount 详细资料 设置 新手区"
        print
        u'昵称: ' + num_name

        str_intro = driver.find_element_by_xpath("//div[@class='pf_intro']")
        str_t = str_intro.text.split(" ")
        num_intro = str_t[0]  # 空格分隔 获取第一个值 "Eastmount 详细资料 设置 新手区"
        print
        u'简介: ' + num_intro

        # Error:  'unicode' object is not callable
        # 一般是把字符串当做函数使用了 str定义成字符串 而str()函数再次使用时报错
        try:
            str_wb = driver.find_element_by_xpath("//td[1]/a[@class='t_link S_txt1']/strong")
        except:
            str_wb = driver.find_element_by_xpath("//td[@class='S_line1'][1]/strong")
        pattern = r"\d+\.?\d*"  # 正则提取"微博[0]" 但r"(\[.*?\])"总含[]
        guid = re.findall(pattern, str_wb.text, re.S | re.M)
        for value in guid:
            num_wb = int(value)
            break
        print
        u'关注数: ' + str(num_wb)

        # 关注数
        try:
            str_gz = driver.find_element_by_xpath("//td[2]/a[@class='t_link S_txt1']/strong")
        except:
            str_gz = driver.find_element_by_xpath("//td[@class='S_line1'][2]/strong")
        guid = re.findall(pattern, str_gz.text, re.M)
        num_gz = int(guid[0])
        print
        u'粉丝数: ' + str(num_gz)

        # 粉丝数
        try:
            str_fs = driver.find_element_by_xpath("//td[3]/a[@class='t_link S_txt1']/strong")
        except:
            str_fs = driver.find_element_by_xpath("//td[@class='S_line1'][3]/strong")
        guid = re.findall(pattern, str_fs.text, re.M)
        num_fs = int(guid[0])
        print
        u'微博数: ' + str(num_fs)

        # ***************************************************************************
        # No.2 文件操作写入信息
        # ***************************************************************************

        infofile.write('=====================================================================\r\n')
        infofile.write(u'用户: ' + user_id + '\r\n')
        infofile.write(u'昵称: ' + num_name + '\r\n')
        infofile.write(u'简介: ' + num_intro + '\r\n')
        infofile.write(u'微博数: ' + str(num_wb) + '\r\n')
        infofile.write(u'关注数: ' + str(num_gz) + '\r\n')
        infofile.write(u'粉丝数: ' + str(num_fs) + '\r\n')
        infofile.write(u'微博内容: ' + '\r\n')

        # ***************************************************************************
        # No.3 获取微博内容
        # http://weibo.cn/guangxianliuyan?filter=0&page=1
        # 其中filter=0表示全部 =1表示原创
        # ***************************************************************************

        print
        '\n'
        print
        u'获取微博内容信息'
        num = 1
        while num <= 5:
            url_wb = "http://weibo.com/" + user_id + "?filter=0&page=" + str(num) + "&is_all=1"  # 0所有微博 1原创微博
            print
            url_wb
            driver.get(url_wb)
            for i in range(15):
                info = driver.find_elements_by_xpath("//div[@class='WB_feed WB_feed_v3 WB_feed_v4']/div[" + str(
                    i + 2) + "]//div[@class='WB_text W_f14']")
                for value in info:
                    info = value.text
                    print
                    info
                    if info.startswith(u'转发', 0, len(info)) or info.startswith(u'//', 0, len(info)):
                        print
                        u'转发微博'
                        infofile.write(u'[转发微博]\r\n' + info + '\r\n')
                    else:
                        print
                        u'原创微博'
                        infofile.write(u'[原创微博]\r\n' + info + '\r\n')

            print
            u'next page...\n'
            infofile.write('\r\n\r\n')
            num += 1
            print
            '\n\n'
        print
        '**********************************************'


    except Exception as e:
        print
        "Error: ", e
    finally:
        print
        u'VisitPersonPage!\n\n'
        print
        '**********************************************\n'


# *******************************************************************************
#                                程序入口 预先调用
# *******************************************************************************

if __name__ == '__main__':

    # 定义变量
    username = '******'  # 输入你的微博用户名
    password = '******'  # 输入你的密码
    user_id = 'guangxianliuyan'  # 用户id url+id访问个人

    # 操作函数
    LoginWeibo(username, password)  # 登陆微博

    # driver.add_cookie({'name':'name', 'value':'_T_WM'})
    # driver.add_cookie({'name':'value', 'value':'c86fbdcd26505c256a1504b9273df8ba'})

    # 注意
    # 因为sina微博增加了验证码,但是你用Firefox登陆一次输入验证码,再调用该程序即可,因为Cookies已经保证
    # 会直接跳转到明星微博那部分,即: http://weibo.cn/guangxianliuyan

    # 在if __name__ == '__main__':引用全局变量不需要定义 global inforead 省略即可
    print
    'Read file:'
    user_id = inforead.readline()
    while user_id != "":
        user_id = user_id.rstrip('\r\n')
        VisitPersonPage(user_id)  # 访问个人页面
        user_id = inforead.readline()
        # break

    infofile.close()
    inforead.close()
