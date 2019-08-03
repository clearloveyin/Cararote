# -*- coding:utf-8 -*-
import re
from XlsUtil import XlsUtil

class XlsCoverInfo:
    def __init__(self, cover_sheet):
        self.cover_sheet = cover_sheet
        #start from 1
        self.row_max = cover_sheet.UsedRange.Rows.Count + 1
        # start from 1
        self.col_max = cover_sheet.UsedRange.Columns.Count + 1
        self.CHAPTER_PATTERN = '''\s*第.*章\s*'''
        self.VER_PATTERN = '''^(Ver|ver).*\d+\..*'''

    def make_cover_info(self, ret_dict):
        cover_sheet = self.cover_sheet
        for ir in range(1,self.row_max):
            row_str = ""
            for ic in range(1,self.col_max):
                cell_str = XlsUtil().get_cell_str_value(cover_sheet, ir ,ic)
                if cell_str:
                    row_str+=cell_str

            if row_str == "":
                continue

            if re.match(self.CHAPTER_PATTERN ,row_str):
                ret_dict["chapterInfo"] = row_str
            elif re.match(self.VER_PATTERN ,row_str):
                ret_dict["verInfo"] = row_str
            else:
                ret_dict["titleInfo"] = row_str