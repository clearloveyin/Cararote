# -*- coding:utf-8 -*-
from PIL import ImageGrab
import os
import re

class XlsUtil:
    def __init__(self):
        self.xlEdgeLeft = 7
        self.xlEdgeTop = 8
        self.xlEdgeBottom = 9
        self.xlEdgeRight = 10
        self.xlEdgeRight = 10
        self.xlDiagonalUp = 6
        self.xlDiagonalDown = 5

    def get_cell_str_value(self, sheet_info, row, col):
        try:
            cell_str_val = sheet_info.Cells(row, col).Value
            if not cell_str_val:
                return None
            if isinstance(cell_str_val, str) == True:
                return cell_str_val.encode("utf8").strip()
            elif isinstance(cell_str_val, unicode) == True:
                return cell_str_val.encode("utf8").strip()
            else:
                return str(cell_str_val).strip()
        except Exception as e_info:
            print e_info
            return None

    def get_cell_border_str(self, sheet_info, row, col):
        try:
            cell_info =sheet_info.Cells(row, col)
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
        except Exception as e_info:
            print e_info
            return ""

        return ret_border_str

    def cap_range_as_img(self, sheet_info, img_dir, img_file, s_row, s_col, e_row, e_col):
        cap_cells = sheet_info.Range(sheet_info.Cells(s_row, s_col),
                                     sheet_info.Cells(e_row, e_col))
        try:
            cap_cells.CopyPicture(1, 2)
        except Exception:
            print "copy cell error:", img_file
            return False

        image_info = ImageGrab.grabclipboard()
        if image_info:
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            image_info.save((r"%s\%s") % (img_dir, img_file))
            return True
        else:
            print "grab error:", img_file
            return False

    def check_is_table_row(self, sheet_info, row_no, s_col, e_col):
        row_str = ""
        for ic in range(s_col, e_col + 1):
            row_str += self.get_cell_border_str(sheet_info, row_no, ic)
            if self.get_cell_str_value(sheet_info, row_no, ic):
                row_str += "A"
        tablePattern = '''.+(/|\|)$'''
        if re.match(tablePattern, row_str):
            return True
        else:
            return False

