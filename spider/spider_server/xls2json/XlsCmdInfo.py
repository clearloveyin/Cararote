# -*- coding:utf-8 -*-
from XlsUtil import XlsUtil
import re

class XlsCmdInfo:
    def __init__(self,cmd_sheet):
        self.cmd_sheet = cmd_sheet
        self.cmd_info_col = 2
        self.func_info_col = 7
        self.cmd_valid_col = 13
        self.make_cmd_info_col()

    def make_cmd_info_col(self):
        cmd_sheet = self.cmd_sheet
        st_row = 8
        for ir in range(st_row, st_row+3):
            for ic in range(2, 21):
                cell_str = XlsUtil().get_cell_str_value(cmd_sheet, ir, ic)
                if cell_str and cell_str.find("客先仕様書情報")>=0:
                    self.cmd_info_col = ic
                elif cell_str and cell_str.find("社内仕様書")>=0:
                    self.func_info_col = ic
                elif cell_str and cell_str.find("客先仕様書落とし込み判断")>=0:
                    self.cmd_valid_col = ic

    def make_cmd_head_info(self, info_dict):
        cmd_sheet = self.cmd_sheet
        info_dict["req_spec"] = ""
        info_dict["spec_no"] = ""
        info_dict["version"] = ""
        info_dict["article"] = ""
        info_dict["cmd_filename"] = ""
        if XlsUtil().get_cell_str_value(cmd_sheet, 3, 4):
            info_dict["req_spec"] = XlsUtil().get_cell_str_value(cmd_sheet, 3, 4)
        if XlsUtil().get_cell_str_value(cmd_sheet, 4, 4):
            info_dict["spec_no"] = XlsUtil().get_cell_str_value(cmd_sheet, 4, 4)
        if XlsUtil().get_cell_str_value(cmd_sheet, 5, 4):
            info_dict["version"] = XlsUtil().get_cell_str_value(cmd_sheet, 5, 4)
        if XlsUtil().get_cell_str_value(cmd_sheet, 6, 4):
            info_dict["article"] = XlsUtil().get_cell_str_value(cmd_sheet, 6, 4)
        if XlsUtil().get_cell_str_value(cmd_sheet, 7, 4):
            info_dict["cmd_filename"] = XlsUtil().get_cell_str_value(cmd_sheet, 7, 4)

    def make_cmd_relation_info(self, info_dict):
        cmd_sheet = self.cmd_sheet
        func_doc_pattern = "^func(_\d+)+.*"
        func_chapter_pattern = "^\d+(\.\d+)+(\.|\s)\D+"
        info_dict["relation_info"] = []

        for ir in range(10, cmd_sheet.UsedRange.Rows.Count+1):
            func_doc_info = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col+2)
            if not func_doc_info:
                continue
            bFound_func_doc = False
            for doc_data in func_doc_info.split("\n"):
                if re.match(func_doc_pattern, doc_data):
                    bFound_func_doc = True
                    break

            if bFound_func_doc == False:
                continue

            relation_dict = {}
            relation_dict["cmd_chapter_no"] = ""
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col):
                relation_dict["cmd_chapter_no"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col)
            relation_dict["cmd_chapter_title"] = ""
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col+1):
                relation_dict["cmd_chapter_title"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col+1)
            relation_dict["cmd_page"] = ""
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col + 2):
                relation_dict["cmd_page"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col + 2)
            relation_dict["cmd_update_date"] = ""
            if self.cmd_info_col + 3 < self.func_info_col and XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col + 3):
                relation_dict["cmd_update_date"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_info_col + 3)

            relation_dict["func_no_list"] = []
            relation_dict["func_doc_list"] = []
            relation_dict["func_ver_list"] = []
            relation_dict["func_chapter_list"] = []
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 1):
                for cell_str in XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 1).split("\n"):
                    relation_dict["func_no_list"].append(cell_str)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 2):
                for cell_str in XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 2).split("\n"):
                    relation_dict["func_doc_list"].append(cell_str)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 3):
                for cell_str in XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 3).split("\n"):
                    relation_dict["func_ver_list"].append(cell_str)

            chapter_info_str = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 5)
            if (not chapter_info_str) or (len(chapter_info_str) == 0) or (chapter_info_str=="-"):
                chapter_info_str = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.func_info_col + 4)
                if (not chapter_info_str) or (len(chapter_info_str) == 0) or (chapter_info_str=="-"):
                    continue

            chapter_info_str = chapter_info_str.replace("\n","")

            if re.match(func_chapter_pattern, chapter_info_str):
                split_char_index_list = []
                split_info_match = re.match(func_chapter_pattern, chapter_info_str)
                i_split_index = 0
                while split_info_match:
                    split_info = split_info_match.group(0)
                    split_char_index_list.append(chapter_info_str.index(split_info))
                    i_split_index += len(split_info)
                    split_info_match = re.match(func_chapter_pattern, chapter_info_str[i_split_index:])
                split_char_index_list.append(len(chapter_info_str))

                for i_split_info in range(0,len(split_char_index_list)-1):
                    relation_dict["func_chapter_list"].append(chapter_info_str[split_char_index_list[i_split_info]:split_char_index_list[i_split_info+1]])
            else:
                relation_dict["func_chapter_list"].append(chapter_info_str)

            relation_dict["cmd_valid_info"] = ""
            relation_dict["cmd_valid_reason"] = ""
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col):
                relation_dict["cmd_valid_info"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+1):
                relation_dict["cmd_valid_reason"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+1)

            relation_dict["author_depart"] = ""
            relation_dict["author_group"] = ""
            relation_dict["author_name"] = ""
            relation_dict["author_write_date"] = ""
            relation_dict["author_comment"] = ""
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+2):
                relation_dict["author_depart"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+2)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+3):
                relation_dict["author_group"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+3)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+4):
                relation_dict["author_name"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+4)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+5):
                relation_dict["author_write_date"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+5)
            if XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+6):
                relation_dict["author_comment"] = XlsUtil().get_cell_str_value(cmd_sheet, ir, self.cmd_valid_col+6)

            info_dict["relation_info"].append(relation_dict)