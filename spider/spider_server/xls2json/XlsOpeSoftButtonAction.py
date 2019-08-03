# -*- coding:utf-8 -*-
from XlsUtil import XlsUtil
import re

class XlsOpeSoftButtonAction:
    def __init__(self, ope_sheet, img_dir, ope_no):
        self.ope_sheet = ope_sheet
        self.img_dir = img_dir
        self.ope_no = ope_no
        self.start_row = 4
        self.start_col = 2
        self.end_row = ope_sheet.UsedRange.Rows.Count
        self.get_row_range()
        self.number_pattern = "^\d.*"

    def get_row_range(self):
        ope_sheet = self.ope_sheet
        screen_no = ""

        for ir in range(self.start_row, self.end_row + 1):
            if not XlsUtil().get_cell_str_value(ope_sheet, ir, 3):
                continue
            line_str = []
            line_str.append(XlsUtil().get_cell_str_value(ope_sheet, ir, 3))
            if line_str[0].lower() == "soft button action":
                self.start_row = ir
                screen_no = XlsUtil().get_cell_str_value(ope_sheet, ir, 2)
                break

        for ir in range(self.start_row+1, self.end_row+1):
            if not XlsUtil().get_cell_str_value(ope_sheet, ir, 2):
                continue
            if XlsUtil().get_cell_str_value(ope_sheet, ir, 2) != screen_no:
                self.end_row = ir
                break

    def make_soft_btn_action(self, content_list):
        ope_sheet = self.ope_sheet

        soft_btn_action_dict = {}
        soft_btn_action_dict["title_info"] = "Soft Button Action"

        img_file_name = "%sR%d.jpg" % (self.ope_no, self.start_row+1)
        if XlsUtil().cap_range_as_img(ope_sheet, self.img_dir, img_file_name, self.start_row+1,
                                      3, self.end_row - 1, 49) == True:
            soft_btn_action_dict["action_info"] = ('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)

        content_list.append(soft_btn_action_dict)
