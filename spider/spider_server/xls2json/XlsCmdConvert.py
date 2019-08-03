# -*- coding:utf-8 -*-
import json
import win32com.client
from XlsCmdInfo import XlsCmdInfo
import os

def do_path_convert(path_dir):
    for parent, dirs, files in os.walk(path_dir):
        for i_f, file_name in enumerate(files,1):
            full_file_name = os.path.join(parent, file_name)
            xlApp = win32com.client.Dispatch('Excel.Application')
            xlApp.Visible = False
            try:
                xlBook = xlApp.Workbooks.Open(full_file_name)
            except:
                print "error:",full_file_name
                xlApp.Quit()
                continue

            for i_sheet in xlBook.Sheets:
                cmd_result_dict = {}
                cmd_result_dict["file_name"] = file_name.decode("gbk").encode("utf8")
                xls_cmd_info = XlsCmdInfo(i_sheet)
                xls_cmd_info.make_cmd_head_info(cmd_result_dict)
                xls_cmd_info.make_cmd_relation_info(cmd_result_dict)

                json.dump(cmd_result_dict, open(r"C:\Users\yuyin\Desktop\Func_Android\func_json\%s_%d.json" % (
                    parent.split("\\")[-1], i_f), "wb"), ensure_ascii=False, indent=2, encoding='utf-8')
            xlBook.Close(0)
            xlApp.Quit()


if __name__ == '__main__':
    #import sys
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    do_path_convert(r"C:\Users\yuyin\Desktop\Func_Android")

    # xlApp = win32com.client.Dispatch('Excel.Application')
    # xlApp.Visible = False
    # xlBook = xlApp.Workbooks.Open(r"C:/sharedoc/tmp/cmd/025/17CY_System_ Specification.xlsx")
    # for i_f, i_sheet in enumerate(xlBook.Sheets, 1):
    #     cmd_result_dict = {}
    #     xls_cmd_info = XlsCmdInfo(i_sheet)
    #     xls_cmd_info.make_cmd_head_info(cmd_result_dict)
    #     xls_cmd_info.make_cmd_relation_info(cmd_result_dict)
    #
    #     json.dump(cmd_result_dict, open(r"C:/sharedoc/tmp/ttt.json","wb"),ensure_ascii=False, indent=2)

    #xlBook.Close(0)
    #xlApp.Quit()

    print "dump finish"

