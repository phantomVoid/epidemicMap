import time, requests, json


def is_number(s):
    if s is None:
        return False
    else:
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
    return False


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
url = 'https://c.m.163.com/ug/api/wuhan/app/index/feiyan-data-list?t=%d' % int(time.time() * 1000)
result = requests.get(url, headers=headers)
assign = result.json()['data']['list']

count = 0
for index in range(len(assign)):
    if assign[index]['province'] == '福建':
        cur = assign[index]['confirm']
        if is_number(cur):
            cur = assign[index]['confirm']
        else:
            cur = 0
        print('省:{0:s}, 市: {1:s}, 确诊: {2:n}'.format(assign[index]['province'], assign[index]['name'], cur))
        count = count + cur
print('\n总数: {0:n}'.format(count))
# todo: indent缩进空格间距，sort_keys按照key来排序,ensure_ascii解码显示中文
json_str = json.dumps(assign, indent=4, sort_keys=False, ensure_ascii=False)
