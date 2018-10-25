#!/usr/bin/python3
import os
import shutil
A = os.getcwd() + '/bcm/'
C = os.getcwd() + '/1/'
#print (A)
os.chdir(A)
for x in os.listdir('.'):
    print (x)
    B = input('输入文件名:') + '.bcm'
    os.rename(A + x, B)
    shutil.copy (A + B, C)