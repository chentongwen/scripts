#!/usr/bin/python3
import xlrd
import json
import os
import io
import shutil
import codecs
file = "app.xlsx"
data = xlrd.open_workbook(file)
table = data.sheets()[0]
nrows = table.nrows
returnData = {}
for i in range(nrows):
    sourDir = os.getcwd()
    path = os.getcwd() + '/dist/'
    #print path
    content = table.row_values(i)
    key = content[9]
    pkgInfo = {
        "url": content[10],
        "execName": content[9],
        "displayName": content[1],
        "chinaName": content[0],
        "GenericName": content[0],
#        "comment": content[4],
        "chinacomment": content[3],
        "desktopName": content[9],
        "icon": content[9],
        "categories": content[2],
        "version": content[11],
        "width": content[12],
        "height": content[13],
        "flash": content[14],
    }
    #if len(content[14]) != 0:
    #    pkgInfo["flash"] = content[14]
    #else:
    #    pkgInfo["flash"] = 
    if content[17] == 'webapp' or content[17] == 'java' or content[17] == 'bcm':
        icondir = os.getcwd() + '/icons/allicons/'
        bcmDir = os.getcwd() + '/bcm/'
        #print icondir
        file_name = path + key + '/'
        #print file_name
        try:
            os.makedirs(file_name)
        except:
            pass
        finally:
            with codecs.open (file_name + '/app.json', 'w') as text:
                json.dump(pkgInfo, text, ensure_ascii=False, indent=2)
            shutil.copy(icondir + key + '.svg', file_name)
            shutil.copy(bcmDir + key +".bcm", file_name)
            try:
                if content[17] == 'webapp':
                    shutil.copy("app.sh", file_name)
                    shutil.copytree("electron", file_name + "electron")
                    os.chdir(file_name)
                    os.system('./app.sh')
                    os.chdir(sourDir)
                    print(key + '___' + 'success')
                elif content[17] == 'java':
                    shutil.copy("java.sh", file_name)
                    os.chdir(file_name)
                    os.system('./java.sh')
                    os.chdir(sourDir)
                elif content[17] == 'bcm':
                    shutil.copy("bcm.sh", file_name)
                    os.chdir(file_name)
                    os.system('./bcm.sh')
                    os.chdir(sourDir)
                else:
                    print (key + '错误')
            except IOError as msg:
                print(msg)
                print(key + '_______' + 'OK')