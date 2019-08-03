# -*- coding:utf-8 -*-
import win32com.client
import json
import os
import shutil
from XlsUtil import XlsUtil
from XlsOpeHeadInfo import XlsOpeHeadInfo
from XlsOpeScreenViewInfo import XlsOpeScreenViewInfo
from XlsOpeSoftButtonInfo import XlsOpeSoftButtonInfo
from XlsOpeSoftButtonAction import XlsOpeSoftButtonAction
from XlsOpeHardKeyAction import XlsOpeHardKeyAction
from XlsOpeScreenStatus import XlsOpeScreenStatus
from XlsOpeStatusChange import XlsOpeStatusChange
from XlsOpeTransition import XlsOpeTransition
from XlsOpeTriggerAction import XlsOpeTriggerAction

if __name__ == '__main__':
    ope_result = {}
    file_name = r"C:\Users\yuyin\Desktop\Func_Android\Morley_Func_01_Radio.xlsx"

    ope_result["fileName"] = file_name.split("/")[-1].split(".")[0]
    img_dir = r"C:\\sharedoc\\tmp\\" + ope_result["fileName"]
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
    os.system("md %s" % (img_dir))

    xlApp = win32com.client.Dispatch('Excel.Application')
    if xlApp.Version < 15.0:
        print "Please install office 2013"
        exit(1)
    xlApp.Visible = False
    xlBook = xlApp.Workbooks.Open(file_name)

    ope_result["screen_list"] = []

    for i_sheet in xlBook.Sheets:
        chapter_dict = {}

        info_list = []
        for ic in range(1, i_sheet.UsedRange.Columns.Count+1):
            if XlsUtil().get_cell_str_value(i_sheet, 2, ic):
                info_list.append(XlsUtil().get_cell_str_value(i_sheet, 2, ic))
        chapter_dict["screen_no"] = info_list[0]
        chapter_dict["screen_name"] = info_list[1]
        chapter_dict["content_list"] = []

        XlsOpeHeadInfo(i_sheet, img_dir, chapter_dict["screen_no"]).make_head_info(chapter_dict["content_list"])
        XlsOpeScreenViewInfo(i_sheet, img_dir, chapter_dict["screen_no"]).make_screen_view_info(chapter_dict["content_list"])
        XlsOpeSoftButtonInfo(i_sheet, img_dir, chapter_dict["screen_no"]).make_soft_btn_view_info(chapter_dict["content_list"])
        XlsOpeSoftButtonAction(i_sheet, img_dir, chapter_dict["screen_no"]).make_soft_btn_action(chapter_dict["content_list"])
        XlsOpeHardKeyAction(i_sheet, img_dir, chapter_dict["screen_no"]).make_hard_key_action(chapter_dict["content_list"])
        XlsOpeScreenStatus(i_sheet, img_dir, chapter_dict["screen_no"]).make_screen_status(chapter_dict["content_list"])
        XlsOpeStatusChange(i_sheet, img_dir, chapter_dict["screen_no"]).make_status_change(chapter_dict["content_list"])
        XlsOpeTransition(i_sheet, img_dir, chapter_dict["screen_no"]).make_transition_info(chapter_dict["content_list"])
        XlsOpeTriggerAction(i_sheet, img_dir, chapter_dict["screen_no"]).make_trigger_action(chapter_dict["content_list"])

        ope_result["screen_list"].append(chapter_dict)

    xlBook.Close(0)
    xlApp.Quit()

    json.dump(ope_result, open(r"C:/sharedoc/tmp/%s.json" % (ope_result["fileName"]), "wb"),
              ensure_ascii=False, indent=2)

    print "dump finish"