# encoding=utf8
import http
import hashlib
import urllib.request
import random
import json
import sys
import os
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
while True:
    # fin = open(r'E:\pyCharmSpaces\epidemicMap\txt\04 第四部-445后.txt', 'r', encoding='UTF-8')
    # fout = open(r'E:\pyCharmSpaces\epidemicMap\txt\translated\04 第四部-445后.txt', 'w', encoding='UTF-8')  # 以写的方式打开输出文件

    fin = open(r'/com/phantom/demo/txt\04-貴族院の自称図書委員.txt', 'r', encoding='UTF-8')  # 以读的方式打开输入文件
    fout = open(r'/com/phantom/demo/txt\translated\第四部-贵族院自称图书委员.txt', 'w', encoding='UTF-8')  # 以写的方式打开输出文件
    for eachLine in fin:
        appid = '20200223000387699'  # 参考百度翻译后台，申请appid和secretKey
        secretKey = 'wiFFrTTOSKgE0v3xeCgY'
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q = eachLine.strip()  # 文本文件中每一行作为一个翻译源
        fromLang = 'jp'  # 日语
        toLang = 'zh'  # 中文
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        sign = sign.encode('UTF-8')
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        html = response.read().decode('UTF-8')
        target2 = json.loads(html)
        # print(target2.get("trans_result"))
        try:
            src = target2["trans_result"][0]["dst"]
            print(src)  # 取得翻译后的文本结果,测试可删除注释
            outStr = src
            fout.write(outStr.strip() + '\n')
        except:
            pass
    fin.close()
    fout.close()
    print('翻译成功，请查看文件')
    path = '/com/phantom/demo/txt\\translated'
    os.system("start explorer %s" % path)
    break