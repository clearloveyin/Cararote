# -*- coding:utf-8 -*-
from XlsUtil import XlsUtil
import re

class XlsOpeSoftButtonInfo:
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
            if line_str[0].lower() == "view of soft button":
                self.start_row = ir
                screen_no = XlsUtil().get_cell_str_value(ope_sheet, ir, 2)
                break

        for ir in range(self.start_row+1, self.end_row+1):
            if not XlsUtil().get_cell_str_value(ope_sheet, ir, 2):
                continue
            if XlsUtil().get_cell_str_value(ope_sheet, ir, 2) != screen_no:
                self.end_row = ir
                break

    def get_one_part_range(self, s_row, e_row):
        ope_sheet = self.ope_sheet
        one_part_s = -1
        one_part_e = -1

        if s_row+1 == e_row:
            return one_part_s, one_part_e

        one_part_no = ""
        if XlsUtil().get_cell_str_value(ope_sheet, s_row, 3):
            one_part_no = XlsUtil().get_cell_str_value(ope_sheet, s_row, 3)
            one_part_s = s_row
        else:
            return one_part_s, one_part_e

        for ir in range(one_part_s+1, e_row):
            one_part_e = ir
            if not XlsUtil().get_cell_str_value(ope_sheet, ir, 3):
                continue
            if XlsUtil().get_cell_str_value(ope_sheet, ir, 3) != one_part_no:
                break

        # the last line
        if one_part_e+1 == e_row:
            one_part_e = e_row

        return one_part_s, one_part_e

    def make_soft_btn_view_info(self, content_list):
        soft_btn_view_dict = {}
        soft_btn_view_dict["title_info"] = "View of Soft Button"

        view_content_e_row = self.make_reference_info(soft_btn_view_dict)
        if view_content_e_row == -1:
            view_content_e_row = self.end_row

        one_part_s_row, one_part_e_row = self.get_one_part_range(self.start_row+1, view_content_e_row)
        soft_btn_view_dict["content_list"] = []
        while one_part_s_row > 0 and one_part_e_row > 0:
            one_part_dict = {}
            #print one_part_s_row, one_part_e_row
            self.make_one_part_info(one_part_s_row, one_part_e_row, one_part_dict)
            one_part_s_row, one_part_e_row = self.get_one_part_range(one_part_e_row, view_content_e_row)
            soft_btn_view_dict["content_list"].append(one_part_dict)

        content_list.append(soft_btn_view_dict)

    def make_reference_info(self, screen_view_dict):
        ope_sheet = self.ope_sheet
        ref_s_row = -1
        ref_e_row = -1

        if  XlsUtil().get_cell_str_value(ope_sheet, self.end_row-1, 3):
            if not re.match(self.number_pattern, XlsUtil().get_cell_str_value(ope_sheet, self.end_row-1, 3)):
                ref_e_row = self.end_row-1
            else:
                return -1
        else:
            return -1

        for ir in range(ref_e_row, self.start_row, -1):
            if XlsUtil().get_cell_str_value(ope_sheet, ir, 3):
                if not re.match(self.number_pattern, XlsUtil().get_cell_str_value(ope_sheet, ir, 3)):
                    ref_s_row = ir
                else:
                    break
            else:
                break

        if ref_s_row > 0:
            img_file_name = "%sR%d.jpg" % (self.ope_no, ref_s_row)
            if XlsUtil().cap_range_as_img(ope_sheet, self.img_dir, img_file_name, ref_s_row,
                                          3, ref_e_row, 49) == True:
                screen_view_dict["reference"] = ('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)

        return ref_s_row

    def make_one_part_info(self, part_s_row, part_e_row, one_part_dict):
        ope_sheet = self.ope_sheet
        one_part_dict["title_info"] = ""
        one_part_dict["action_info"] = ""

        if XlsUtil().get_cell_str_value(ope_sheet, part_s_row, 4):
            one_part_dict["title_info"] = XlsUtil().get_cell_str_value(ope_sheet, part_s_row, 4)

        action_info_s_row = part_s_row+1

        if action_info_s_row == part_e_row:
            return

        img_file_name = "%sR%d.jpg" % (self.ope_no, action_info_s_row)
        if XlsUtil().cap_range_as_img(ope_sheet, self.img_dir, img_file_name, action_info_s_row,
                                      4, part_e_row-1, 49) == True:
            one_part_dict["action_info"] = ('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)
