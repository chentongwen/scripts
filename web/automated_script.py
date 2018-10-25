#!/usr/bin/env python3
import xlrd
import codecs
import os
import shutil
import stencil
import subprocess
#print ('2222')
xlsx_file = "app.xlsx"
data = xlrd.open_workbook(xlsx_file)
table = data.sheets()[0]
nrows = table.nrows
returnData = {}
for i in range(nrows):
#    sourDir = os.getcwd() + '/'##脚本所在的路径
#    IconsDir = sourDir + '/icons/allicons/'##图标所在的路径
#    SAVE_PATH = sourDir + 'dist/'##结果存放的路径

    #print path
    #print ('1111111')
    content = table.row_values(i)
    KEY = content[9]
    URL = content[10]
    pkgInfo = {
        "url": content[10],
        "execName": content[9],
        "displayName": content[1],
        "chinaName": content[0],
        "GenericName": content[0],
        "comment": content[4],
        "chinacomment": content[3],
        "desktopName": content[9],
        "icon": content[9],
        "categories": content[2],
        "VERSION": content[11],
        "width": content[12],
        "height": content[13],
        "keywords": content[5],
#        "flash": content[14],
    }
    #判断是否使用flash
    if len(content[14]) != 0:
        pkgInfo["flash"] = content[14]
    else:
        pkgInfo["flash"] = "null",
    if content[17] == 'webapp' or content[17] == 'java' or content[17] == 'swf' or content[17] == 'bcm':
        ##nativefier.json文件
        nativefier_web = stencil.NATIVEFIER_WEB.substitute(**pkgInfo)
        nativefier_swf = stencil.NATIVEFIER_SWF.substitute(**pkgInfo)
        ##package的json文件
        package_json = stencil.PACKAGE_JSON.substitute(**pkgInfo)
        ##desktop文件
        desktop_web = stencil.DESKTOP_WEB.format(**pkgInfo)
        desktop_java = stencil.DESKTOP_JAVA.format(**pkgInfo)
        #desktop_swf = stencil.DESKTOP_SWF.format(**pkgInfo)
        desktop_bcm = stencil.DESKTOP_BCM.format(**pkgInfo)
        ##swf 的inject文件模板
        inject_js = stencil.INJECT_JS.substitute(**pkgInfo)
        ##metadata.yaml文件
        yaml_web = stencil.YAML_WEB.format(**pkgInfo)
        yaml_java = stencil.YAML_JAVA.format(**pkgInfo)
        yaml_swf = stencil.YAML_SWF.format(**pkgInfo)
        yaml_bcm = stencil.YAML_BCM.format(**pkgInfo)
    #print (pac)
        sourDir = os.getcwd() + '/'##脚本所在的路径
        IconsDir = sourDir + 'icons/'##图标所在的路径
        SAVE_PATH = sourDir + 'dist/' + KEY##结果存放的路径
        print (SAVE_PATH)
        try:
            os.makedirs(SAVE_PATH)
        except:
            print ('此文件已经存在')
        shutil.copy(IconsDir + KEY + '.svg', SAVE_PATH)
        try:
            ##生成webapp包
            if content[17] == 'webapp':
                shutil.copytree("electron",os.path.join(SAVE_PATH+"/electron"))
                with codecs.open(os.path.join(SAVE_PATH+'/electron/nativefier.json'),'w')as A:
                    A.write(nativefier_web)
                with codecs.open(os.path.join(SAVE_PATH+'/electron/package.json'),'w')as B:
                    B.write(package_json)
                with codecs.open(os.path.join(SAVE_PATH+'/metadata.yaml'),'w')as C:
                    C.write(yaml_web)
                with codecs.open(os.path.join(SAVE_PATH+'/'+KEY+'.desktop'),'w')as D:
                    D.write(desktop_web)
                subprocess.check_call('asar pack '+os.path.join(SAVE_PATH+'/electron')+' '+os.path.join(SAVE_PATH+'/'+KEY+'.asar'),shell=True)
                subprocess.check_call('rm -r '+os.path.join(SAVE_PATH+'/electron'),shell=True)
                print (KEY+'===========================OK')
            ##生成java包
            elif content[17] == 'java':
                with codecs.open(os.path.join(SAVE_PATH+'/'+KEY+'.desktop'),'w')as A:
                    A.write(desktop_java)
                with codecs.open(os.path.join(SAVE_PATH+'/metadata.yaml'),'w')as B:
                    B.write(yaml_java)
                subprocess.check_call('wget '+URL+' -O '+os.path.join(SAVE_PATH+'/'+KEY+'.jar'),shell=True)
                #bcm包
            elif content[17] == 'bcm':
                with codecs.open(os.path.join(SAVE_PATH+'/'+KEY+'.desktop'),'w')as A:
                    A.write(desktop_bcm)
                with codecs.open(os.path.join(SAVE_PATH+'/metadata.yaml'),'w')as B:
                    B.write(yaml_bcm)
            ##生成swf包
            elif content[17] == 'swf':
                subprocess.check_call('wget '+content[10]+' -O '+SAVE_PATH+'/'+KEY+'.swf', shell=True)
                #shutil.copy(os.path.join(sourDir+'swf/'+KEY+'.swf'),SAVE_PATH)
                shutil.copytree("electron",os.path.join(SAVE_PATH+"/electron"))
                with codecs.open(os.path.join(SAVE_PATH+'/electron/inject/inject.js'),'w')as inject:
                    inject.write(inject_js)
                with codecs.open(os.path.join(SAVE_PATH+'/electron/nativefier.json'),'w')as A:
                    A.write(nativefier_swf)
                with codecs.open(os.path.join(SAVE_PATH+'/electron/package.json'),'w')as B:
                    B.write(package_json)
                with codecs.open(os.path.join(SAVE_PATH+'/metadata.yaml'),'w')as C:
                    C.write(yaml_swf)
                with codecs.open(os.path.join(SAVE_PATH+'/'+KEY+'.desktop'),'w')as D:
                    D.write(desktop_web)
                subprocess.check_call('asar pack '+os.path.join(SAVE_PATH+'/electron')+' '+os.path.join(SAVE_PATH+'/'+KEY+'.asar'),shell=True)
                subprocess.check_call('rm -r '+os.path.join(SAVE_PATH+'/electron'),shell=True)
        except IOError as msg:
            print (msg)
        #break