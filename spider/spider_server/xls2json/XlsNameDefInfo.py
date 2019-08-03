# -*- coding:utf-8 -*-
import re

class XlsNameDefInfo:
    def __init__(self, name_def_sheet):
        self.name_def_sheet = name_def_sheet
        # start from 1
        self.row_max = name_def_sheet.UsedRange.Rows.Count + 1
        # start from 1
        self.col_max = 33
        self.CHAPTER_PATTERN = '''^\d+\.\d+.*'''
        self.xlEdgeLeft = 7
        self.xlEdgeTop = 8
        self.xlEdgeBottom = 9
        self.xlEdgeRight = 10

    def make_name_def_info(self, ret_dict):
        name_def_sheet = self.name_def_sheet
        ret_dict["nameDefInfo"] = {}
        table_start_row=self.get_table_first_row()
        if  table_start_row <= 0:
            return
        table_col_list = []
        for ic in range(1, self.col_max):
            if self.get_xls_string_value(name_def_sheet.Cells(table_start_row, ic).Value):
                table_col_list.append(ic)
        ret_dict["nameDefInfo"]["nameDefList"]=[]

        for ir in range(table_start_row, self.row_max):
            row_str_list = []
            for ic in table_col_list:
                if self.get_xls_string_value(name_def_sheet.Cells(ir, ic).Value):
                    row_str_list.append(self.get_xls_string_value(name_def_sheet.Cells(ir, ic).Value))
                else:
                    row_str_list.append("")
            if ir == table_start_row or "" not in row_str_list:
                row_str_dict = {}
                row_str_dict["nameInfo"] = [self.get_data_dict(ir,table_col_list[0])]
                row_str_dict["nameDef"] = [self.get_data_dict(ir,table_col_list[1])]
                ret_dict["nameDefInfo"]["nameDefList"].append(row_str_dict)
                continue
            else:
                for i_str in range(0,len(row_str_list)):
                    if len(row_str_list[i_str]) == 0:
                        continue
                    if i_str == 0:
                        ret_dict["nameDefInfo"]["nameDefList"][-1]["nameInfo"]\
                            .append(self.get_data_dict(ir,table_col_list[i_str]))
                    else:
                        ret_dict["nameDefInfo"]["nameDefList"][-1]["nameDef"] \
                            .append(self.get_data_dict(ir,table_col_list[i_str]))

    def get_table_first_row(self):
        name_def_sheet = self.name_def_sheet
        for ir in range(1, self.row_max):
            row_str=""
            for ic in range(1, self.col_max+1):
                now_cell = name_def_sheet.Cells(ir, ic)
                if not name_def_sheet.Cells(ir, ic).Value:
                    continue
                if now_cell.Borders.Item(self.xlEdgeLeft).LineStyle > 0:
                    row_str+="|"
                if now_cell.Borders.Item(self.xlEdgeTop).LineStyle > 0:
                    row_str += "-"
                if now_cell.Borders.Item(self.xlEdgeBottom).LineStyle > 0:
                    row_str += "_"
                if now_cell.Borders.Item(self.xlEdgeRight).LineStyle > 0:
                    row_str += "|"
                row_str += "A"
                tablePattern = '''.*(-|_).*A(\|)?(-|_).+'''
                if re.match(tablePattern, row_str):
                    return ir
        return 0

    def get_data_dict(self, row_no, col_no):
        name_def_sheet = self.name_def_sheet
        cell_str = self.get_xls_string_value(name_def_sheet.Cells(row_no, col_no).Value)
        if not cell_str:
            cell_str = ""
        ret_dict = {}
        ret_dict["dataType"] = "STR"
        ret_dict["dataValue"] = [cell_str]
        return ret_dict

    def get_xls_string_value(self, xls_value):
        if not xls_value:
            return None
        if isinstance(xls_value, str) == True:
            return xls_value.encode("utf8")
        elif isinstance(xls_value, unicode) == True:
            return xls_value.encode("utf8")
        else:
            return str(xls_value)