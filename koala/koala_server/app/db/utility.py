# -*- coding: UTF-8 -*-
import os, sys, platform
import string
from io import BytesIO
import urllib.request
from urllib.parse import quote
from PIL import Image
from PIL import BmpImagePlugin,GifImagePlugin,Jpeg2KImagePlugin,JpegImagePlugin,PngImagePlugin,TiffImagePlugin,WmfImagePlugin # added this line
from PIL import ImageChops
from sqlalchemy.schema import Sequence
from flask import current_app
from app.db import db


class Utillity():
    def __init__(self):
        pass

    @staticmethod
    def get_nextval(seq='image_id_seq'):
        try:
            # CREATE SEQUENCE image_id_seq START 1;
            nextid = db.session.execute(Sequence(seq))
            return nextid
        except Exception as e:
            current_app.logger.info("[Sequence: %s]" % (e))
            return None

    @staticmethod
    def split_ext_name(full_file_name):
        file_name, ext_name = os.path.splitext(full_file_name)
        return file_name, ext_name

    @staticmethod
    def get_new_file_name(full_file_name, _id):
        file_name, ext_name = os.path.splitext(full_file_name)
        file_name = '_'.join([file_name, str(_id)])
        new_file_name = ''.join([file_name, ext_name])
        return new_file_name

    @staticmethod
    def emf_to_jpeg(self, emf_imag_file):
        Image._initialized = 2  # added this line
        f, e = os.path.splitext(emf_imag_file)
        outfile = f + ".jpg"
        if emf_imag_file != outfile:
            im = Image.open(emf_imag_file).convert('RGB')
            im.save(outfile, "JPEG")  # added "JPEG"
            im.close()
            del im
        return outfile

    @staticmethod
    def get_new_version(new_ver=None, old_ver=None):
        if not old_ver and not old_ver:
            return '0.001'
        if new_ver and not old_ver:
            return new_ver
        if new_ver > old_ver:
            return new_ver

        # if (old_ver and not new_ver) or (old_ver == new_ver):
        vers = old_ver.split('.')
        new_vers = []
        carry_val = 1
        for ver in vers[::-1]:
            ver_len = len(ver)
            ver = int(ver) + carry_val
            if sys.version_info.major >= 3:  # Python >= 3
                carry_val = ver // (10 ** ver_len)
            else:
                carry_val = ver / (10 ** ver_len)
            temp_new_ver = str(ver % (10 ** ver_len))
            new_vers.append(temp_new_ver.zfill(ver_len))
        new_ver = '.'.join(new_vers[::-1])
        return new_ver

    @staticmethod
    def convert_url(srv_url, file_url):
        expanduser = os.path.expanduser('~')
        if file_url.startswith(expanduser):
            expanduser = os.path.join(expanduser, 'data')
            file_url = file_url[len(expanduser):]
            file_url = file_url.strip(os.path.sep)
        else:
            _, file_url = os.path.splitdrive(file_url)  # 去掉盘符
            file_url = file_url.strip(os.path.sep)
            file_url = file_url.replace('\\', '/')
        url = '/'.join([srv_url, file_url])
        return url

    @staticmethod
    def diff_image(path_one, path_two):
        """
        比较两张图片是否相同
        :param image_one:
        :param image_two:
        :return: True/Flase
        """
        try:
            path_one = Utillity.resolve_http_image(path_one)
            path_two = Utillity.resolve_http_image(path_two)
            image_one = Image.open(path_one)
            image_two = Image.open(path_two)
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:
                # 图片间没有任何不同则返回True
                return True
            else:
                return False
        except:
            # 旧地址可能找不到图片了或者比较出错，此时返回False
            return False

    @staticmethod
    def resolve_http_image(image_url):
        """
        解析服务器上的图片
        :param image_url:
        :return: 图片的内容
        """
        if "http:" in image_url:
            image_url = image_url.replace('\\', '/')
            image_url = image_url.replace(' ', '%20')
            image_url = quote(image_url, safe=string.printable)
            image_content = BytesIO(urllib.request.urlopen(image_url).read())
        else:
            image_content = image_url
        return image_content

def main():
    # new_file_name = Utillity.get_new_file_name('a.txt', 1)
    # print(new_file_name)
    # print(Utillity.get_new_version('', ''))
    # print(Utillity.get_new_version('0.001', ''))
    # print(Utillity.get_new_version('0.001', '0.002'))
    print(Utillity.get_new_version('0.003', '0.001'))


if __name__ == '__main__':
    main()
