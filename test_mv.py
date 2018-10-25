#!/usr/bin/python3
import os
import shutil
PATH = os.getcwd()
path = PATH + '/dist/'
Dir = PATH + '/fourteen/'
Scr = path + 'screenshots/'
#a = screenshots
#print (PATH)
#print (path)
for x in os.listdir(Dir + '/logo/'):
    NAME = x.replace('_logo.svg','')
    #print (NAME)
    try:
        os.makedirs(path + NAME + '/screenshots')
    except:
        pass
    shutil.copy(Dir + 'logo/' + NAME + '_logo.svg',path + NAME + '/' + NAME + '.svg' )
    shutil.copy(Dir + 'cover/' + NAME + '_cover.png', path + NAME)
    shutil.copy(Dir + 'screenshots/' + NAME + '/screenshots/' + NAME  + '_1.png',path + NAME + '/screenshots/')
    shutil.copy(Dir + 'screenshots/' + NAME + '/screenshots/' +NAME + '_2.png',path + NAME + '/screenshots/')
    shutil.copy(Dir + 'screenshots/' + NAME + '/screenshots/' + NAME + '_3.png',path + NAME + '/screenshots/')