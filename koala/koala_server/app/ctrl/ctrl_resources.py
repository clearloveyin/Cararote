# -*- coding: UTF-8 -*-
import copy
import json
import os
from flask import current_app
from app.db import db
from sqlalchemy import or_, and_
from app.ctrl.ctrl_base import CtrlBase
from app.db.resources import *
from app.db.projects import *
from app.ctrl.utility import Utillity
INPUT_STATUS_DEL = '0'  # 删除
INPUT_STATUS_NOR = '1'  # 正常


class CtrlResources(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def import_file(self, request_data):
        try:
            if not request_data.files:
                return False, '没有上传文件!'
            file_upload = request_data.files['file']
            commiter = request_data.form.get('commit_user')
            if not db.session.query(Projects).filter(Projects.proj_id == request_data.form.get('proj_id')).all():
                return False, '没有此项目!'
            proj = db.session.query(Projects).filter(Projects.proj_id == request_data.form.get('proj_id')).first()
            file_name = file_upload.filename
            file_name = file_name.replace(' ', '').replace('(', '').replace(')', '')
            curr_app = current_app._get_current_object()
            uti = Utillity()
            # fun_seq_fun_id_seq;
            # file_seq_file_id_seq
            # Utillity.get_nextval('fun_seq_fun_id_seq')
            only_id = uti.get_nextval("file_seq_file_id_seq")
            file_path = os.path.abspath(os.path.join(os.getcwd(), r'data', r'temp', str(only_id)))
            # file_path = os.path.abspath(os.path.join(os.getcwd(), r'data', r'temp'))
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_upload.save(os.path.join(file_path, file_name))

            new_path = os.path.join(curr_app.config.get('SPEC_PATH_ROOT'), proj.insideName.inside_name,
                                    request_data.form.get('type'), str(request_data.form.get('version_id')))
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            mv = 'mv %s %s' % (os.path.join(file_path, file_name), new_path)
            os.system(mv)
            inputs = db.session.query(InputResourceInfo).filter(InputResourceInfo.resource_id == request_data.form.get("resource_id")).all()
            url = Utillity.convert_url('', new_path)
            new_url = os.path.join(url, file_name)
            if not inputs:
                self.add_one_to_table(proj.proj_id, request_data.form.get('type'), file_name, commiter,
                                      new_url, request_data.form.get('version_id'))
                return True, ""
            else:
                repeat = self.find_input_repeat(inputs[0].resource_id, request_data.form.get('version_id'))
                if repeat:
                    db.session.rollback()
                    return False, '此版本已存在!'
                self.upload_to_table(new_url, commiter, inputs[0].resource_id, request_data.form.get('version_id'))
                return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def add_one_to_table(self, proj_id, res_type, filename, commiter, url, res_ver):
        res_info = {InputResourceInfo.proj_id.name: proj_id,
                    InputResourceInfo.resource_type.name: res_type,
                    InputResourceInfo.file_name.name: filename,
                    InputResourceInfo.commit_time.name: self.get_current_time(),
                    InputResourceInfo.update_user_id.name: commiter,
                    InputResourceInfo.status.name: INPUT_STATUS_NOR
                    }
        attach = InputResourceInfo(**res_info)
        db.session.add(attach)
        db.session.flush()
        ver_info = {
                InputResourceData.url.name: url,
                InputResourceData.user_id.name: commiter,
                InputResourceData.resource_id.name: attach.resource_id,
                InputResourceData.version_id.name: res_ver,
                InputResourceData.commit_time.name: self.get_current_time(),
                InputResourceData.status.name: INPUT_STATUS_NOR,
        }
        attach2 = InputResourceData(**ver_info)
        db.session.add(attach2)
        db.session.commit()

    def upload_to_table(self, url, commiter, resource_id, res_ver):
        ver_info = {
            InputResourceData.url.name: url,
            InputResourceData.user_id.name: commiter,
            InputResourceData.resource_id.name: resource_id,
            InputResourceData.version_id.name: res_ver,
            InputResourceData.commit_time.name: self.get_current_time(),
            InputResourceData.status.name: INPUT_STATUS_NOR,
        }
        attach2 = InputResourceData(**ver_info)
        db.session.add(attach2)
        db.session.commit()

    def find_input_repeat(self, resource_id, ver):
        IRD = (db.session.query(InputResourceData)
               .filter(InputResourceData.resource_id == resource_id)
               .filter(InputResourceData.version_id == ver)
               .all())
        if IRD:
            return True
        else:
            return False

    def import_txt(self, request_data):
        try:
            data = request_data.get_json(force=True)
            commiter = data.get('commit_user')
            txt = data.get('text')
            title = data.get('title')
            if not db.session.query(Projects).filter(Projects.proj_id == data.get('proj_id')).all():
                return False, '没有此项目!'
            proj = db.session.query(Projects).filter(Projects.proj_id == data.get('proj_id')).first()
            inputs = db.session.query(InputResourceInfo).filter(
                InputResourceInfo.resource_id == data.get("resource_id")).all()
            if not inputs:
                self.add_one_to_table(proj.proj_id, data.get('type'), title, commiter,
                                      txt, data.get('version_id'))
                return True, ""
            else:
                repeat = self.find_input_repeat(inputs[0].resource_id, data.get('version_id'))
                if repeat:
                    db.session.rollback()
                    return False, '此版本已存在!'
                self.upload_to_table(txt, commiter, inputs[0].resource_id, data.get('version_id'))
                return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_input_by_quotation_id(self, quotation_id):
        inputs = (db.session.query(ResourceQuotation)
                  .filter(ResourceQuotation.quotation_id == quotation_id)
                  .all())
        resource_list = []
        for i_input in inputs:
            resource_list.append({
                "input_name": i_input.resource_data.resourceInfo.file_name,
                "type": i_input.resource_data.resourceInfo.resource_type,
                "version": i_input.resource_data.version_id,
                "url": i_input.resource_data.url,
            })
        return True, resource_list

    def get_input_by_proj_id(self, proj_id, _type):
        try:
            curr_app = current_app._get_current_object()
            FILE_SRV_URL = curr_app.config.get('FILE_SRV_URL')
            resource_list = []
            q = (db.session.query(InputResourceInfo)
                 .filter(InputResourceInfo.proj_id == proj_id)
                 .filter(InputResourceInfo.resource_type == _type)
                 .filter(InputResourceInfo.status == INPUT_STATUS_NOR)
                 .all())
            for input_info in q:
                ver_list = []
                input_data_list = input_info.input_resource_data
                for input_data in input_data_list:
                    if input_data.status == INPUT_STATUS_DEL:
                        continue
                    if _type == "FILE":
                        url = '/'.join([FILE_SRV_URL, input_data.url])
                    else:
                        url = input_data.url
                    ver_list.append({"id": input_data.id,
                                     "version_id": input_data.version_id,
                                     "url": url})
                resource_list.append({
                    "resource_id": input_info.resource_id,
                    "resource_name": input_info.file_name,
                    "type": input_info.resource_type,
                    "ver_list": ver_list
                })
            return True, resource_list
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_resource_list_all(self):
        return

    def del_input(self, resource_id, resource_data_id):
        try:
            if resource_data_id:
                q = (db.session.query(InputResourceData)
                     .filter(InputResourceData.id == resource_data_id)
                     .filter(InputResourceData.resource_id == resource_id)
                     .first())
                if q:
                    q.status = INPUT_STATUS_DEL
                    db.session.commit()
                else:
                    return False, 'Input 版本 ID[%s]不存在, 或者已经被删除了。' % resource_data_id
            else:
                q = (db.session.query(InputResourceInfo)
                     .filter(InputResourceInfo.resource_id == resource_id)).first()
                if q:
                    q.status = INPUT_STATUS_DEL
                    db.session.commit()
                else:
                    return False, 'Input Info ID[%s]不存在' % resource_id
            return True, "删除成功！"

        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"



