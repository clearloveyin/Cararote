# -*- coding:utf-8 -*-
import win32com.client
from XlsCoverInfo import XlsCoverInfo
from XlsNameDefInfo import XlsNameDefInfo
from XlsFunctionInfo import XlsFunctionInfo
from XlsChapterInfo import XlsChapterInfo
import json
import os
import shutil
import re

def recursive_chapter_info(chapter_list, xls_file_name, sheet_name_list, xlBook):
    for chapter_data in chapter_list:
        if len(chapter_data["subChapterList"]) > 0:
            recursive_chapter_info(chapter_data["subChapterList"], xls_file_name, sheet_name_list, xlBook)

        if chapter_data["titleInfo"]=="Outline":
            for sheet_name in sheet_name_list:
                if re.match('''[\d|\s|\.]*Outline\s*''', sheet_name.encode("utf8")):
                    #print sheet_name.encode("utf8")
                    i_sheet = xlBook.Worksheets(sheet_name)
                    XlsFunctionInfo(i_sheet, img_dir).make_function_info(chapter_data)
                    break
        elif chapter_data["titleInfo"].find("用語定義") >=0:
            for sheet_name in sheet_name_list:
                if sheet_name.encode("utf8").find("用語定義") >= 0:
                    #print sheet_name.encode("utf8")
                    i_sheet = xlBook.Worksheets(sheet_name)
                    XlsNameDefInfo(i_sheet).make_name_def_info(chapter_data)
                    break
        else:
            bFound = False
            chapter_hyperlink = chapter_data["hypterlink"]
            re_need_transfer_str = [("*","\*"),(".","\."),("?","\?"),("+","\+"),("$","\$"),("^","\^"),("[","\["),
                                    ("]","\]"),("(","\("),(")","\)"),("{","\{"),("}","\}"),("|","\|"),("/","\/")]

            for sheet_name in sheet_name_list:
                if chapter_hyperlink.find(sheet_name.encode("utf8")) >= 0:
                    #print sheet_name.encode("utf8")
                    bFound = True
                    i_sheet = xlBook.Worksheets(sheet_name)
                    XlsFunctionInfo(i_sheet, img_dir).make_function_info(chapter_data)
                    break

                re_chapter_data = chapter_data["chapterInfo"]
                re_title_data = chapter_data["titleInfo"][0]

                for before_char, after_char in re_need_transfer_str:
                    re_chapter_data = re_chapter_data.replace(before_char,after_char)
                    re_title_data = re_title_data.replace(before_char, after_char)

                do_sheet_pattern = "^%s.?%s" % (re_chapter_data, re_title_data)
                #print do_sheet_pattern
                if re.match(do_sheet_pattern, sheet_name.encode("utf8")):
                    #print sheet_name.encode("utf8")
                    bFound = True
                    i_sheet = xlBook.Worksheets(sheet_name)
                    XlsFunctionInfo(i_sheet, img_dir).make_function_info(chapter_data)
                    # json.dumps(chapter_data, ensure_ascii=False, indent=2)
                    break

            if bFound == False:
                print "eeeeeeee", chapter_data["chapterInfo"], chapter_data["titleInfo"]

        chapter_data.pop("hypterlink")


if __name__ == '__main__':
    xls_result_dict = {}
    file_name = r"C:/sharedoc/tmp/func/func_5_7_09_G-BOOK_CDF.xlsm"

    xls_result_dict["fileName"] = file_name.split("/")[-1].split(".")[0]
    img_dir = r"C:\\sharedoc\\tmp\\"+xls_result_dict["fileName"]
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
    os.system("md %s"%(img_dir))

    xlApp = win32com.client.Dispatch('Excel.Application')
    if xlApp.Version < 15.0:
        print "Please install office 2013"
        exit(1)
    print "Office Version:" + xlApp.Version
    xlApp.Visible = False
    xlBook = xlApp.Workbooks.Open(file_name)
    sheet_name_list = []
    for i_sheet in xlBook.Sheets:
        sheet_name_list.append(i_sheet.Name)

    for sheet_name in sheet_name_list:
        if sheet_name.encode("utf8").find("表紙") >= 0:
            i_sheet = xlBook.Worksheets(sheet_name)
            XlsCoverInfo(i_sheet).make_cover_info(xls_result_dict)
        elif sheet_name.encode("utf8").find("目次") >= 0:
            i_sheet = xlBook.Worksheets(sheet_name)
            xls_result_dict["chapterInfoList"] = []
            XlsChapterInfo(i_sheet).make_chapter_info(xls_result_dict["chapterInfoList"])
        # elif sheet_name.encode("utf8").find("2.1.2.4.地図注記(地図記号)") >= 0:
        #     i_sheet = xlBook.Worksheets(sheet_name)
        #     func_info_dict = {}
        #     func_info_dict["chapterInfo"] = "2.1.2.4."
        #     XlsFunctionInfo(i_sheet, img_dir).make_function_info(func_info_dict)
        #     #XlsNameDefInfo(i_sheet).make_name_def_info(func_info_dict)
        #     json.dump(func_info_dict, open(r"C:/sharedoc/tmp/rr.json", "wb"), ensure_ascii=False, indent=2)
        #     break

    recursive_chapter_info(xls_result_dict["chapterInfoList"], file_name, sheet_name_list, xlBook)

    xlBook.Close(0)
    xlApp.Quit()

    json.dump(xls_result_dict, open(r"C:/sharedoc/tmp/%s.json"%(xls_result_dict["fileName"]), "wb"), ensure_ascii=False, indent=2)
    print "dump finish"
