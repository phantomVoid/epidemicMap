import os, re, time, pyexiv2
from PIL import Image
import pytesseract


class exif():
    def imgSave(self, dirname):
        for filename in os.listdir(dirname):
            path = dirname + filename
            if os.path.isdir(path):
                path += '/'
                self.imgSave(path)
            else:
                self.imgExif(path)

    def imgExif(self, path):
        try:
            text = pytesseract.image_to_string(Image.open(path), lang='chi_sim')
            string = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", text)
            print(string)
            img_tag = pyexiv2.Image(path)
            img_tag.modify_exif({"Exif.Image.ImageDescription": string})
            img_tag.modify_iptc({"Iptc.Application2.Caption":string})
            print('图片' + path + '写入成功')
        except Exception as e:
            print(e)
            print('图片' + path + '写入失败')

    def start(self):
        _path = input("请输入图片路径：").strip()
        self.imgSave(_path + '\\')


Exif_info = exif()
Exif_info.start()
