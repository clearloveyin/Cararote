# -*- coding:utf-8 -*-
import re
from XlsUtil import XlsUtil

class XlsChapterInfo:
    def __init__(self, chapter_sheet):
        self.chapter_sheet = chapter_sheet
        self.model_info_list = []
        self.chapter_start_row = 10
        # start from 1
        self.row_max = chapter_sheet.UsedRange.Rows.Count
        self.col_max = chapter_sheet.UsedRange.Columns.Count

        self.model_start_col = 34
        self.make_mode_info_list()

        self.chapter_no_col = 2
        self.chapter_name_l1 = 6
        self.chapter_name_l2 = 12
        self.chapter_name_l3 = 18
        self.chapter_name_l4 = -1
        self.chapter_no_col_str = "項番"
        self.chapter_name_l1_str = "大項目"
        self.chapter_name_l2_str = "中項目"
        self.chapter_name_l3_str = "小項目"
        self.chapter_name_l4_str = "細項目"
        self.chk_chapter_col_info()
        self.chapter_done_list = []

    def make_mode_info_list(self):
        chapter_sheet = self.chapter_sheet
        model_end_col = self.col_max+1
        model_end_row=9

        for ic in range(self.model_start_col, model_end_col):
            cell_str = XlsUtil().get_cell_str_value(chapter_sheet, model_end_row, ic)
            if cell_str:
                self.model_start_col = ic
                break
        for ic in range(model_end_col, self.model_start_col, -1):
            cell_str = XlsUtil().get_cell_str_value(chapter_sheet, model_end_row, ic)
            if cell_str:
                model_end_col = ic
                break

        latest_str = ""
        for ic in range(self.model_start_col, model_end_col+1):
            cell_str = XlsUtil().get_cell_str_value(chapter_sheet, 4, ic)
            if cell_str:
                latest_str = cell_str
            self.model_info_list.append(latest_str)

        for i_row in [5,6,8,9]:
            latest_str = ""
            for i_list, ic in enumerate(range(self.model_start_col, model_end_col + 1)):
                cell_str = XlsUtil().get_cell_str_value(chapter_sheet, i_row, ic)
                if cell_str:
                    latest_str = cell_str
                if len(latest_str) > 0:
                    self.model_info_list[i_list] += "-"
                    self.model_info_list[i_list] += latest_str

        self.model_info_list = [model_data.replace("\n", "") for model_data in self.model_info_list]

    def chk_chapter_col_info(self):
        chapter_sheet = self.chapter_sheet
        chk_chapter_col_row = 9
        for ic in range(self.chapter_no_col, self.model_start_col):
            cell_str = XlsUtil().get_cell_str_value(chapter_sheet, chk_chapter_col_row, ic)
            if cell_str:
                if cell_str == self.chapter_no_col_str:
                    self.chapter_no_col = ic
                elif cell_str == self.chapter_name_l1_str:
                    self.chapter_name_l1 = ic
                elif cell_str == self.chapter_name_l2_str:
                    self.chapter_name_l2 = ic
                elif cell_str == self.chapter_name_l3_str:
                    self.chapter_name_l3 = ic
                elif cell_str == self.chapter_name_l4_str:
                    self.chapter_name_l4 = ic

    def make_chapter_info(self, chapter_list):
        self.get_chapter_info(self.chapter_start_row,self.row_max,self.chapter_name_l1, chapter_list)

    def get_chapter_info(self,s_row,e_row,level_col, chapter_list):
        one_level_cat_list = []
        one_level_start_row = s_row
        one_level_next_row = self.find_onelevel_row(one_level_start_row, e_row, level_col)
        while one_level_next_row > 0:
            one_level_cat_list.append((one_level_start_row, one_level_next_row - 1))
            one_level_start_row = one_level_next_row
            one_level_next_row = self.find_onelevel_row(one_level_start_row, e_row, level_col)
        one_level_cat_list.append((one_level_start_row, e_row))

        for ol_start_row, ol_end_row in  one_level_cat_list:
            one_level_chapter_list = []

            next_level_row, next_level_col = self.find_nextlevel_func_row_col(ol_start_row, ol_end_row, level_col)
            if next_level_row == -1 or next_level_col==-1:
                self.make_chapter_data(ol_start_row, ol_end_row, level_col, one_level_chapter_list)
            elif next_level_row == ol_start_row:
                self.make_chapter_data(ol_start_row, next_level_row, level_col, one_level_chapter_list)
                if len(one_level_chapter_list) > 0:
                    self.get_chapter_info(next_level_row, ol_end_row, next_level_col,
                                          one_level_chapter_list[-1]["subChapterList"])
            else:
                self.make_chapter_data(ol_start_row, next_level_row-1, level_col, one_level_chapter_list)
                if len(one_level_chapter_list) > 0:
                    self.get_chapter_info(next_level_row, ol_end_row, next_level_col, one_level_chapter_list[-1]["subChapterList"])
            chapter_list.extend(one_level_chapter_list)

    def make_chapter_data(self,s_row, e_row, level_col, chapter_info_list):
        chapter_sheet = self.chapter_sheet
        for ir in (range(s_row,e_row+1)):
            title_info =XlsUtil().get_cell_str_value(chapter_sheet, ir, level_col)
            if not title_info:
                continue
            if len(title_info) == 0:
                continue
            chapter_no_info = XlsUtil().get_cell_str_value(chapter_sheet,ir,self.chapter_no_col)
            if not chapter_no_info:
                continue
            if len(chapter_no_info) == 0:
                continue
            if chapter_no_info == self.chapter_no_col_str:
                continue
            if (title_info,chapter_no_info) in self.chapter_done_list:
                continue
            if chapter_no_info.find("*") >= 0:
                continue

            for i_find_str_col in range(level_col+1, self.model_start_col-1):
                cell_str = XlsUtil().get_cell_str_value(chapter_sheet, ir, i_find_str_col)
                if cell_str and len(cell_str)>0:
                    chapter_no_info = ""
                    break

            for i_find_hypelink_col in range(level_col, self.model_start_col):
                chapter_hypterlinks = chapter_sheet.Range(chapter_sheet.Cells(ir, i_find_hypelink_col)
                                                          , chapter_sheet.Cells(ir, i_find_hypelink_col)).Hyperlinks
                if i_find_hypelink_col != level_col and XlsUtil().get_cell_str_value(chapter_sheet, ir, i_find_hypelink_col):
                    chapter_hypterlinks = None
                    break
                if chapter_hypterlinks.Count > 0:
                    break

            cat_info_dict = {}
            cat_info_dict["chapterInfo"] = chapter_no_info
            cat_info_dict["titleInfo"] = title_info
            cat_info_dict["modelList"] = []
            self.make_model_info(s_row, cat_info_dict["modelList"])
            cat_info_dict["subChapterList"] = []
            cat_info_dict["hypterlink"] = ""
            if chapter_hypterlinks:
                for i_hyperlink in range(1, chapter_hypterlinks.Count+1):
                    cat_info_dict["hypterlink"]+=chapter_hypterlinks.Item(i_hyperlink).SubAddress.encode("utf8")
            chapter_info_list.append(cat_info_dict)
            self.chapter_done_list.append((title_info,chapter_no_info))

    def make_model_info(self, row_no, model_list):
        if row_no < 10:
            return
        chapter_sheet = self.chapter_sheet

        for i_model in range(0, len(self.model_info_list)):
            model_str = XlsUtil().get_cell_str_value(chapter_sheet, row_no, i_model + self.model_start_col)
            if not model_str:
                model_str = ""
            model_dict = {}
            model_dict[self.model_info_list[i_model]]=model_str
            model_list.append(model_dict)

    def find_nextlevel_func_row_col(self, s_row, e_row, now_level_col):
        chapter_sheet = self.chapter_sheet
        if now_level_col == self.chapter_name_l3 and self.chapter_name_l4 == -1:
            return -1,-1
        if now_level_col == self.chapter_name_l1:
            next_level_col = self.chapter_name_l2
        elif now_level_col == self.chapter_name_l2:
            next_level_col = self.chapter_name_l3
        else:
            next_level_col = self.chapter_name_l4

        for ir in range(s_row, e_row + 1):
            title_info = XlsUtil().get_cell_str_value(chapter_sheet, ir, next_level_col)
            if title_info and len(title_info) > 0:
                chapter_no_info = XlsUtil().get_cell_str_value(chapter_sheet, ir, self.chapter_no_col)
                if not chapter_no_info:
                    continue
                if len(chapter_no_info) == 0:
                    continue
                if chapter_no_info == self.chapter_no_col_str:
                    continue
                if chapter_no_info.find("*") >= 0:
                    continue
                return ir, next_level_col

        return -1,-1

    def find_onelevel_row(self, s_row, e_row, onelevel_col):
        chapter_sheet = self.chapter_sheet
        for ir in range(s_row+1, e_row+1):
            title_info = XlsUtil().get_cell_str_value(chapter_sheet, ir, onelevel_col)
            if title_info and len(title_info) > 0:
                chapter_no_info = XlsUtil().get_cell_str_value(chapter_sheet, ir, self.chapter_no_col)
                if not chapter_no_info:
                    continue
                if len(chapter_no_info) == 0:
                    continue
                if chapter_no_info == self.chapter_no_col_str:
                    continue
                if chapter_no_info.find("*") >= 0:
                    continue
                return ir

        return -1

