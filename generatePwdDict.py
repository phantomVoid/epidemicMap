import itertools as its
import time


def generate(repeatNum):

    num = '1234567890'
    word = 'abcdefghijklmnopqrstuvwxyz'
    capWord = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    symbol = '!@#$%'
    dic = open('./wifipwd.txt', 'r+')
    dic.truncate()
    str = num + word + capWord + symbol
    wordIts = its.product(num, repeat=repeatNum)
    for index in wordIts:
        dic.write(''.join(index))
        dic.write(''.join('\n'))
        print(index)
    dic.close()
    print("密码字典已生成")

def main():
    start_time = time.time()
    generate(repeatNum)
    end_time = time.time()
    project_time = end_time - start_time
    print('程序用时', project_time)

repeatNum = 8
if __name__ == '__main__':
    main()