# -*- coding: UTF-8 -*-
import os
import re
# import cStringIO, urllib2
from PIL import Image
from io import BytesIO
from urllib.parse import quote
import string
import validators
import urllib.request
from flask import request
from flask import current_app
from flask import send_from_directory
from token_manage import auth
from flask_restful import Resource
from app.db.utility import Utillity


class ApiUploadImage(Resource):
    # @auth.login_required
    def post(self):
        """上传图片
        :return:
        """
        result = {"result": "OK", "content": '', 'error': ''}
        try:
            file_upload = request.files['file']
            file_name = file_upload.filename
            # file_path = os.path.join('data', 'Image')
            curr_app = current_app._get_current_object()
            file_path = curr_app.config.get("IMG_PATH_ROOT")
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            uti = Utillity()
            only_id = uti.get_nextval()
            new_file_name = Utillity.get_new_file_name(file_name, only_id)
            # new_file_name = '%s-%s' % (str(only_id), file_name)
            file_upload.save(os.path.join(file_path, new_file_name))
            file_url = os.path.join(file_path, new_file_name)
            file_url = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), file_url)
            result["content"] = file_url
        except Exception as e:
            current_app.logger.error('%s' % e)
            result["error"] = str(e)
            result['result'] = "NG"
        finally:
            return result


class DownFile(Resource):
    # @auth.login_required
    def get(self, path_info):
        file_name = os.path.basename(path_info)
        path_info = path_info.replace(file_name, '')
        current_app.logger.info('DownLoad file path=%s, %s' %
                                (path_info, file_name))
        data = send_from_directory(os.path.join('../', path_info),
                                   file_name, as_attachment=True)
        return data


class ImageSize(Resource):
    # @auth.login_required
    def get(self, image_url):
        """
        :return: 图片的大小
        """
        result = {"result": "OK", "content": '', 'error': ''}
        try:
            image_url = image_url.replace(' ', '%20')
            url = quote(image_url, safe=string.printable)  # safe表示可以忽略的字
            image_data = BytesIO(urllib.request.urlopen(url).read())
            img = Image.open(image_data)
            img_size = img.size
            size = {"long": img_size[0], "wide": img_size[1]}
            result["content"] = size
        except Exception as e:
            current_app.logger.error('%s' % e)
            result["error"] = str(e)
            result['result'] = "NG"
        return result

