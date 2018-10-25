#!/usr/bin/python3
import xlrd
import json
import os
import io
import shutil
import codecs
x_file = "app.xlsx"
data = xlrd.open_workbook(x_file)
table = data.sheets()[0]
nrows = table.nrows
returnData = {}

DesktopTemplate = """[Desktop Entry]
Name={Name}
Name[zh_CN]={Name_zh_CN}
Comment[zh_CN]={comment_zh_CN}
Icon=/usr/share/pixmaps/{ICON}.svg
Categories={CATEGORIES}
Keywords[zh_CN]={}
Type=Application
Exec=/opt/google/chrome/google-chrome {URL}
"""
for i in range(nrows):
    sourDir = os.getcwd()
    path = os.getcwd() + '/dist/'
    #print path
    content = table.row_values(i)
    KEY = content[9]
    pkgInfo = {
        "URL": content[10],
        "Name": content[1],
        "Name_zh_CN": content[0],
        "comment_zh_CN": content[3],
        "ICON": content[9],
        "keywords": content[5],
        "CATEGORIES": content[2],
    }
    result = DesktopTempl"keywords": content[5],ate.format(**pkgInfo)
    try:
        os.makedirs(path)
    except:
        pass
    finally:
        with codecs.open (path + KEY + '.desktop', 'w') as text:
            text.write(result)
            #json.dump(pkgInfo, text, ensure_ascii=False, indent=2)