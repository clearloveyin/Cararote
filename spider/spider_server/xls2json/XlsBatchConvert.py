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
    if not chapter_list:
        return
    for chapter_data in chapter_list:
        if len(chapter_data["subChapterList"]) > 0:
            recursive_chapter_info(chapter_data["subChapterList"], xls_file_name, sheet_name_list, xlBook)

        # if chapter_data["titleInfo"]=="Outline":
        #     for sheet_name in sheet_name_list:
        #         if re.match('''[\d|\s|\.]*Outline\s*''', sheet_name.encode("utf8")):
        #             #print sheet_name.encode("utf8")
        #             i_sheet = xlBook.Worksheets(sheet_name)
        #             XlsFunctionInfo(i_sheet, img_dir).make_function_info(chapter_data)
        #             break
        elif chapter_data["titleInfo"].find("Term Definition") >=0:
            for sheet_name in sheet_name_list:
                if sheet_name.encode("utf8").find("Term Definition") >= 0:
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
    full_file_name_list = []
    for root, _, files in os.walk(r"C:/Users/yuyin/Desktop/Func_Android"):
        for i_file_name in files:
            file_name = os.path.join(root, i_file_name)
            full_file_name_list.append(file_name)

    for work_file_name in full_file_name_list:
        xls_result_dict = {}
        file_name = work_file_name

        xls_result_dict["fileName"] = file_name.split("\\")[-1].split(".")[0]
        print xls_result_dict["fileName"]
        img_dir = r"C:/Users/yuyin/Desktop/func_json/" + xls_result_dict["fileName"]
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        # os.system("md %s" % (img_dir))
        CHAPTER_PATTERN = '''^\d+\.\d+.*'''

        xlApp = win32com.client.Dispatch('Excel.Application')
        if xlApp.Version < 15.0:
            print "Please install office 2013"
            exit()
        print "Office Version:" + xlApp.Version
        xlApp.Visible = False
        try:
            xlBook = xlApp.Workbooks.Open(file_name)
        except Exception as e:
            print("error file: " + file_name)
            continue
        sheet_name_list = []
        for i_sheet in xlBook.Sheets:
            sheet_name_list.append(i_sheet.Name)

        for sheet_name in sheet_name_list:
            # if sheet_name.encode("utf8").find("表紙") >= 0:
            #     i_sheet = xlBook.Worksheets(sheet_name)
            #     XlsCoverInfo(i_sheet).make_cover_info(xls_result_dict)
            # elif sheet_name.encode("utf8").find("目次") >= 0:
            #     i_sheet = xlBook.Worksheets(sheet_name)
            #     xls_result_dict["chapterInfoList"] = []
            #     XlsChapterInfo(i_sheet).make_chapter_info(xls_result_dict["chapterInfoList"])
            if sheet_name.encode("utf8").find("Contents") >= 0:
                i_sheet = xlBook.Worksheets(sheet_name)
                xls_result_dict["chapterInfoList"] = []
                XlsChapterInfo(i_sheet).make_chapter_info(xls_result_dict["chapterInfoList"])
        recursive_chapter_info(xls_result_dict.get("chapterInfoList"), file_name, sheet_name_list, xlBook)

        xlBook.Close(0)
        xlApp.Quit()
        json.dump(xls_result_dict, open(r"C:/Users/yuyin/Desktop/func_json/%s.json" % (xls_result_dict["fileName"]), "wb"),
                  ensure_ascii=False, indent=2)

    print "dump finish"
