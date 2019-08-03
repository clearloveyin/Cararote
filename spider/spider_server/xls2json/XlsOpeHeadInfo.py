# -*- coding:utf-8 -*-
from XlsUtil import XlsUtil

class XlsOpeHeadInfo:
    def __init__(self, ope_sheet, img_dir, ope_no):
        self.ope_sheet = ope_sheet
        self.img_dir = img_dir
        self.ope_no = ope_no
        self.start_row = 4
        self.start_col = 2
        self.end_row = ope_sheet.UsedRange.Rows.Count

    def make_head_info(self, content_list):
        self.make_outline_info(content_list)
        self.make_model_info(content_list)

    def make_outline_info(self, content_list):
        ope_sheet = self.ope_sheet
        start_outline_row = -1
        end_outline_row = -1
        for ir in range(self.start_row, self.end_row+1):
            if not XlsUtil().get_cell_str_value(ope_sheet, ir, 3):
                continue
            line_str = []
            line_str.append(XlsUtil().get_cell_str_value(ope_sheet, ir, 3))
            if line_str[0].lower() == "outline":
                start_outline_row = ir
            if line_str[0].lower() == "available model":
                end_outline_row = ir
                break

        outline_dict = {}
        outline_dict["title_info"] = "Outline"
        outline_dict["action_info"] = ""
        img_file_name = "%sR%d.jpg" % (self.ope_no, start_outline_row)
        if XlsUtil().cap_range_as_img(ope_sheet, self.img_dir, img_file_name, start_outline_row+1,
                                      3, end_outline_row-1, 49) == True:
            outline_dict["action_info"] = ('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)
        content_list.append(outline_dict)

    def make_model_info(self, content_list):
        ope_sheet = self.ope_sheet

        start_model_row = -1
        end_model_row = -1
        for ir in range(self.start_row, self.end_row + 1):
            if not XlsUtil().get_cell_str_value(ope_sheet, ir, 3):
                continue
            line_str = []
            line_str.append(XlsUtil().get_cell_str_value(ope_sheet, ir, 3))
            if line_str[0].lower() == "available model":
                start_model_row = ir
            if line_str[0].lower() == "view of screen":
                end_model_row = ir
                break

        model_result = {}
        model_result["title_info"] = "Available Model"
        model_result["action_info"] = ""
        img_file_name = "%sR%d.jpg" % (self.ope_no, start_model_row)
        if XlsUtil().cap_range_as_img(ope_sheet, self.img_dir, img_file_name, start_model_row+1,
                                      3, end_model_row-1, 49) == True:
            model_result["action_info"] = ('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)

        content_list.append(model_result)




