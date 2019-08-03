# -*- coding:utf-8 -*-
import re
from PIL import ImageGrab
from XlsUtil import XlsUtil

class XlsFunctionInfo:
    def __init__(self, func_info_sheet, img_dir):
        self.func_info_sheet = func_info_sheet
        self.img_dir = img_dir
        self.CHAPTER_PATTERN = '''^\d+\.\d+.*'''
        # start from 1
        self.row_max = func_info_sheet.UsedRange.Rows.Count
        # start from 1
        self.col_max = func_info_sheet.UsedRange.Columns.Count
        self.fun_content_col = 33
        self.xlEdgeLeft = 7
        self.xlEdgeTop = 8
        self.xlEdgeBottom = 9
        self.xlEdgeRight = 10
        self.xlEdgeRight = 10
        self.xlDiagonalUp = 6
        self.xlDiagonalDown = 5
        self.ref_start_col = self.get_ref_start_col()
        self.update_date_col = self.get_update_date_col()
        self.func_key_list = ["Outline","Precondition","Invocation","Scope of Application","Func","Addition","例外","仕向","Table","図"]
        self.func_type_list = ["SUMMARY", "PRECONDITION", "CALLINFO", "APPRANGE", "FUNCTION", "SUPPLY", "EXCEPT", "DESTINATION", "TABLE", "IMG"]
        self.model_start_col = 40
        self.model_info_list = []
        self.make_mode_info_list()
        self.image_pos_list = []
        self.make_image_pos_info()
        self.chapterInfo=""


    def get_ref_start_col(self):
        func_info_sheet = self.func_info_sheet
        for ir in range(1, self.row_max+1):
            for ic in range(1, self.col_max+1):
                now_cell = XlsUtil().get_cell_str_value(func_info_sheet, ir,ic)
                if now_cell and now_cell.find("参照先仕様書") >= 0:
                    return ic
        return -1

    def get_update_date_col(self):
        func_info_sheet = self.func_info_sheet
        for ir in range(1, self.row_max+1):
            for ic in range(1, self.col_max+1):
                now_cell = XlsUtil().get_cell_str_value(func_info_sheet, ir, ic)
                if now_cell and now_cell.find("更新日") >= 0:
                    return ic
        return -1

    def make_mode_info_list(self):
        func_info_sheet = self.func_info_sheet
        model_end_col = self.col_max + 1
        model_end_row = 9

        for ic in range(self.model_start_col, model_end_col):
            cell_str = XlsUtil().get_cell_str_value(func_info_sheet, model_end_row, ic)
            if cell_str:
                self.model_start_col = ic
                break
        for ic in range(model_end_col, self.model_start_col, -1):
            cell_str = XlsUtil().get_cell_str_value(func_info_sheet, model_end_row, ic)
            if cell_str:
                model_end_col = ic
                break

        latest_str = ""
        for ic in range(self.model_start_col, model_end_col + 1):
            cell_str = XlsUtil().get_cell_str_value(func_info_sheet, 4, ic)
            if cell_str:
                latest_str = cell_str
            self.model_info_list.append(latest_str)

        for i_row in [5, 6, 8, 9]:
            latest_str = ""
            for i_list, ic in enumerate(range(self.model_start_col, model_end_col + 1)):
                cell_str = XlsUtil().get_cell_str_value(func_info_sheet, i_row, ic)
                if cell_str:
                    latest_str = cell_str
                if len(latest_str) > 0:
                    self.model_info_list[i_list] += "-"
                    self.model_info_list[i_list] += latest_str

        self.model_info_list = [model_data.replace("\n", "") for model_data in self.model_info_list]

    def make_image_pos_info(self):
        func_info_sheet = self.func_info_sheet
        for i_shape in range(0,func_info_sheet.Shapes.Count):
            try:
                shape_top_left_row = func_info_sheet.Shapes[i_shape].TopLeftCell.Row
                shape_top_left_col = func_info_sheet.Shapes[i_shape].TopLeftCell.Column
                shape_bottom_right_row = func_info_sheet.Shapes[i_shape].BottomRightCell.Row
                shape_bottom_right_col = func_info_sheet.Shapes[i_shape].BottomRightCell.Column
                self.image_pos_list.append((shape_top_left_row, shape_top_left_col,shape_bottom_right_row,shape_bottom_right_col))
                if shape_bottom_right_row >= self.row_max:
                    self.row_max = shape_bottom_right_row
            except:
                continue

    def get_start_row_col(self):
        func_info_sheet = self.func_info_sheet
        s_row = 1
        s_col = 1
        for ir in range(1, self.row_max+1):
            for ic in range(1, self.fun_content_col+1):
                first_str = XlsUtil().get_cell_str_value(func_info_sheet, ir,ic)
                if first_str:
                    for fun_key in self.func_key_list:
                        if first_str.find(fun_key)==0 and len(self.get_xls_cell_border(func_info_sheet.Cells(ir, ic)))>0:
                            return ir,ic
                    break

        return s_row, s_col

    def make_function_info(self, func_info_dict):
        func_info_dict["funcInfoList"] = []
        self.chapterInfo = func_info_dict["chapterInfo"]
        # if self.ref_start_col < 0 or self.update_date_col < 0:
        #     print "!!sheet is not match template:", self.chapterInfo
        #     self.cap_whole_sheet_as_img(func_info_dict["funcInfoList"])
        #     return
        s_row,s_col = self.get_start_row_col()
        self.get_function_info(s_row, self.row_max, s_col, func_info_dict["funcInfoList"])

    def cap_whole_sheet_as_img(self, func_info_list):
        func_info_sheet = self.func_info_sheet
        img_file_name = "Whole_%d_%d.jpg" % (self.row_max, self.col_max)

        if XlsUtil().cap_range_as_img(func_info_sheet, self.img_dir, img_file_name, \
                                      1,1,self.row_max+1, self.col_max+1) == True:
            info_dict = {}
            info_dict["funcType"] = "IMG"
            info_dict["testType"] = "COMMON"
            info_dict["modelList"] = []
            info_dict["funcContent"] = []
            img_content_dict = {}
            img_content_dict["dataType"] = "IMG"
            img_content_dict["dataValue"] = [('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)]
            info_dict["funcContent"].append([img_content_dict])
            info_dict["subFuncList"] = []
            func_info_list.append(info_dict)

    def get_function_info(self, s_row, e_row, f_col, func_list):
        #get one level index list
        one_level_split_func_list = []
        one_level_start_row = s_row
        one_level_next_row = self.find_onelevel_func_row(one_level_start_row, e_row, f_col)
        while one_level_next_row>0:
            one_level_split_func_list.append((one_level_start_row, one_level_next_row-1))
            one_level_start_row = one_level_next_row
            one_level_next_row = self.find_onelevel_func_row(one_level_start_row, e_row, f_col)
        one_level_split_func_list.append((one_level_start_row, e_row))

        for ol_start_row, ol_end_row in  one_level_split_func_list:
            func_info_dict = {}
            func_info_dict["subFuncList"] = []
            next_level_row, next_level_col = self.find_nextlevel_func_row_col(ol_start_row, ol_end_row, f_col)
            if next_level_row == -1 or next_level_col==-1:
                self.make_info_data(ol_start_row, ol_end_row, f_col, func_info_dict)
            else:
                self.make_info_data(ol_start_row, next_level_row-1, f_col, func_info_dict)
                self.get_function_info(next_level_row, ol_end_row, next_level_col, func_info_dict["subFuncList"])
            func_list.append(func_info_dict)

    def make_info_data(self, info_s_row, info_e_row, info_col, info_dict):
        func_info_sheet = self.func_info_sheet

        info_dict["funcType"]=""
        func_cell_info = XlsUtil().get_cell_str_value(func_info_sheet, info_s_row, info_col)
        if not func_cell_info:
            print self.chapterInfo, "error!!!can not input to db!!!"
            return

        for i_func, fun_key in enumerate(self.func_key_list,0):
            if func_cell_info.find(fun_key) == 0:
                info_dict["funcType"] = self.func_type_list[i_func]
                break

        info_dict["testType"] = "COMMON"
        find_test_cell = func_info_sheet.Cells(info_s_row, 34)
        if find_test_cell.Borders.Item(self.xlDiagonalUp).LineStyle > 0:
            info_dict["testType"] = "CANNOTTEST"
        elif find_test_cell.Borders.Item(self.xlDiagonalDown).LineStyle > 0:
            info_dict["testType"] = "CANNOTTEST"

        info_dict["modelList"] = []
        self.make_model_info(info_s_row,info_dict["modelList"])

        if XlsUtil().get_cell_str_value(func_info_sheet, info_s_row, 2):
            info_dict["ID"] = XlsUtil().get_cell_str_value(func_info_sheet, info_s_row, 2)

        info_dict["funcContent"] = []
        if info_dict["funcType"] =="TABLE":
            self.make_info_table_cotent(info_s_row, info_e_row, info_col,info_dict["funcContent"])
        elif info_dict["funcType"] =="IMG":
            self.make_info_img_cotent(info_s_row, info_e_row, info_col,info_dict["funcContent"])
        else:
            self.make_one_info_content(info_s_row, info_e_row, info_col, info_dict["funcContent"])

    def make_one_info_content(self, func_s_row, func_e_row, func_s_col, content_list):
        func_info_sheet = self.func_info_sheet
        for ir in range(func_s_row, func_e_row + 1):
            row_str_list = []
            row_str_dict_list = []
            w_s_col = func_s_col
            if ir == func_s_row:
                w_s_col = func_s_col+1
            for ic in range(w_s_col, self.fun_content_col+1):
                cell_str = XlsUtil().get_cell_str_value(func_info_sheet, ir,ic)
                if cell_str:
                    row_str_list.append(cell_str)

            for row_str in row_str_list:
                row_str_dict = {}
                row_str_dict["dataType"]="STR"
                row_str_dict["dataValue"] = [row_str]
                row_str_dict_list.append(row_str_dict)

            # ref_info = XlsUtil().get_cell_str_value(func_info_sheet, ir, self.ref_start_col)
            # if ir >= 10 and ref_info:
            #     ref_ver = ""
            #     if XlsUtil().get_cell_str_value(func_info_sheet, ir, self.ref_start_col+1):
            #         ref_ver = XlsUtil().get_cell_str_value(func_info_sheet, ir, self.ref_start_col+1)
            #
            #     for row_str in row_str_list[-1:]:
            #         row_str_dict = {}
            #         row_str_dict["dataType"] = "REFERENCE"
            #         row_str_dict["dataValue"] = [row_str, ref_info, ref_ver]
            #         row_str_dict_list.append(row_str_dict)
            # else:
            #     for row_str in row_str_list[-1:]:
            #         row_str_dict = {}
            #         row_str_dict["dataType"] = "STR"
            #         row_str_dict["dataValue"] = [row_str]
            #         row_str_dict_list.append(row_str_dict)

            if len(row_str_dict_list) > 0:
                content_list.append(row_str_dict_list)

    def make_info_table_cotent(self, func_s_row, func_e_row, func_s_col, content_list):
        func_info_sheet = self.func_info_sheet
        table_row_list = []
        table_col_max = self.fun_content_col
        for ir in range(func_s_row, func_e_row+1):
            if XlsUtil().check_is_table_row(func_info_sheet, ir, func_s_col, table_col_max):
                table_row_list.append(ir)
                # if XlsUtil().get_cell_str_value(func_info_sheet, ir, self.ref_start_col):
                #     table_col_max = self.ref_start_col+1

        if len(table_row_list) == 0:
            self.make_info_img_cotent(func_s_row, func_e_row, func_s_col, content_list)
            return

        if min(table_row_list)>func_s_row:
            self.make_one_info_content(func_s_row, min(table_row_list)-1, func_s_col, content_list)

        img_file_name = "%sR%d.jpg" % (self.chapterInfo, min(table_row_list))
        if XlsUtil().cap_range_as_img(func_info_sheet, self.img_dir, img_file_name, min(table_row_list),
                                      func_s_col, max(table_row_list), table_col_max) == True:
            img_content_dict = {}
            img_content_dict["dataType"] = "IMG"
            img_content_dict["dataValue"] = [('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)]
            content_list.append([img_content_dict])

        if max(table_row_list)+1 < func_e_row:
            self.make_one_info_content(max(table_row_list)+1, func_e_row-1, func_s_col-1, content_list)

    def make_info_img_cotent(self, func_s_row, func_e_row, func_s_col, content_list):
        func_info_sheet = self.func_info_sheet
        pic_pos_list = []

        for pic_s_row,pic_s_col,pic_e_row,pic_e_col in self.image_pos_list:
            if pic_s_row >= func_s_row and pic_s_row<=func_e_row:
                pic_pos_list.append((pic_s_row,pic_s_col,pic_e_row,pic_e_col))

        if len(pic_pos_list) == 0:
            pic_pos_list.append((func_s_row+1,func_s_col, func_e_row-1, self.fun_content_col-1))
            self.make_one_info_content(func_s_row, func_s_row, func_s_col, content_list)
        else:
            self.make_one_info_content(func_s_row, func_s_row + 1, func_s_col, content_list)

        cap_s_row = min([s_row for s_row,_,_,_ in pic_pos_list])
        cap_s_col = min([s_col for _,s_col, _, _ in pic_pos_list])
        cap_e_row = max([e_row for _, _, e_row, _ in pic_pos_list])
        cap_e_col = max([e_col for _, _, _, e_col in pic_pos_list])

        txt_s_row = cap_s_row
        for ir in range(func_s_row+1, cap_s_row):
            for ic in range(func_s_col,self.fun_content_col+1):
                if XlsUtil().get_cell_str_value(func_info_sheet, ir,ic):
                    txt_s_row = ir
                    break
            if (txt_s_row != cap_s_row):
                break
        cap_s_row = txt_s_row

        txt_e_row = cap_e_row
        for ir in range(cap_e_row+1, func_e_row+1):
            for ic in range(func_s_col,self.fun_content_col+1):
                if XlsUtil().get_cell_str_value(func_info_sheet, ir, ic):
                    txt_e_row = ir
                    break
        cap_e_row = txt_e_row

        #print cap_s_row,cap_s_col,cap_e_row,cap_e_col
        img_file_name = "%sR%d.jpg" % (self.chapterInfo, func_s_row)
        if XlsUtil().cap_range_as_img(func_info_sheet, self.img_dir, img_file_name, cap_s_row,
                                      cap_s_col, cap_e_row, cap_e_col) == True:
            img_content_dict={}
            img_content_dict["dataType"]="IMG"
            img_content_dict["dataValue"] = [('''%s/%s''') % (self.img_dir.split("\\")[-1], img_file_name)]
            content_list.append([img_content_dict])
        else:
            print "grab error:",img_file_name

    def make_model_info(self, row_no, model_list):
        if row_no < 10:
            return
        func_info_sheet = self.func_info_sheet

        bFoundModelInfo = False
        for i_model in range(0, len(self.model_info_list)):
            if XlsUtil().get_cell_str_value(func_info_sheet, row_no, i_model+self.model_start_col):
                bFoundModelInfo = True
                break

        if bFoundModelInfo:
            for i_model in range(0, len(self.model_info_list)):
                model_str = XlsUtil().get_cell_str_value(func_info_sheet, row_no, i_model + self.model_start_col)
                if not model_str:
                    model_str = ""
                model_dict = {}
                model_dict[self.model_info_list[i_model]]=model_str
                model_list.append(model_dict)

    def find_onelevel_func_row(self, s_row, e_row, onelevel_col):
        func_info_sheet = self.func_info_sheet
        for ir in range(s_row+1, e_row+1):
            first_str = XlsUtil().get_cell_str_value(func_info_sheet, ir, onelevel_col)
            if first_str:
                for fun_key in self.func_key_list:
                    if first_str.find(fun_key) == 0 and len(self.get_xls_cell_border(func_info_sheet.Cells(ir, onelevel_col)))>0:
                        return ir
        return -1

    def find_nextlevel_func_row_col(self, s_row, e_row, now_level_col):
        func_info_sheet = self.func_info_sheet
        for ir in range(s_row + 1, e_row+1):
            for ic in range(now_level_col+1, self.fun_content_col+1):
                first_str = XlsUtil().get_cell_str_value(func_info_sheet, ir, ic)
                if first_str:
                    for fun_key in self.func_key_list:
                        if first_str.find(fun_key)==0 and len(self.get_xls_cell_border(func_info_sheet.Cells(ir, ic)))>0:
                            return ir,ic
                    break
        return -1,-1

    def get_xls_cell_border(self, cell_info):
        ret_border_str = ""
        if cell_info.Borders.Item(self.xlEdgeLeft).LineStyle > 0:
            ret_border_str += "/"
        if cell_info.Borders.Item(self.xlEdgeTop).LineStyle > 0:
            ret_border_str += "-"
        if cell_info.Borders.Item(self.xlEdgeBottom).LineStyle > 0:
            ret_border_str += "_"
        if cell_info.Borders.Item(self.xlEdgeRight).LineStyle > 0:
            ret_border_str += "|"

        return ret_border_str