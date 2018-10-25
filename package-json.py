#!/usr/bin/env python3
import codecs
import xlrd
import json
import os
import shutil
xfile = "app.xlsx"
mapper = {
    'Literature': 1,
    'Mathematics': 2,
    'English': 3,
    'Physics': 4,
    'Chemistry': 5,
    'Biology': 6,
    'Politics': 7,
    'History': 8,
    'Geography': 9,
    'Music': 10,
    'Art': 11,
    'Science': 12,
    'Computer': 13,
    'Morality': 14,
    'OtherTools': 15
}

type_int={
    'CRX':0,
    'WebApp':1,
    'Linux':2,
    'BCM':3
}
data = xlrd.open_workbook(xfile)
table = data.sheets()[0]
nrows = table.nrows
returnData = {}
for i in range(nrows):
    path = os.getcwd() + '/tar/'

    content = table.row_values(i)
    key = content[9]
    package_json ={
        "packageName": content[9],
        "name": content[0],
        "package": content[9],
        "type": type_int[content[6]],
        "versionNumber": content[11],
        "developer": content[8],
        "officialWebsite": content[16],
        "descr": content[3],
        "icon": content[9] + '_logo.svg',
        "cover": content[9] + '_cover.png',
        "screenshot": [
            content[9] + '_screenshot_1.png',
            content[9] + '_screenshot_2.png',
            content[9] + '_screenshot_3.png'
        ],
        "dependencies": {},
        "scripts": {},
        "labels": [
            {
                "id": mapper[content[2]]
            }
        ]
    }
    #package_json = json.dumps(package_json, ensure_ascii=False, indent=2)
    #print package_json
    file_name = path + key
    source_path = os.getcwd()
    logo_path = source_path + '/logo/'
    cover_path = source_path + '/cover/'
    screenshot_path = source_path + '/screenshots/'
    AA = path + key + '/screenshots'
    BB = path + key + '/' + key
    try:
        os.makedirs(AA)
        os.makedirs(BB)
        #os.makedirs(file_name + '/sceenshot/')
    except:
        pass
    #print (screenshot_path)
    shutil.copy(logo_path + key + '_logo.svg',file_name)
    shutil.copy(cover_path + key + '_cover.png',file_name)
    shutil.copy(screenshot_path + key + '_screenshot_1.png',file_name + '/screenshots/')
    shutil.copy(screenshot_path + key + '_screenshot_2.png',file_name + '/screenshots/')
    shutil.copy(screenshot_path + key + '_screenshot_3.png',file_name + '/screenshots/')
    #file_name = path + key
 
    with codecs.open(file_name + "/" + 'package.json', 'w') as f:
        json.dump(package_json, f, ensure_ascii=False, indent=2)
    print (key + "===============" + 'success')
    #break
    