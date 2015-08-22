#! /usr/bin/python
# coding=UTF-8
'''Uruchamiane gdy serwer się wyłącza'''
from Settings import DATABASE_ROOT
import os
from sys import exit

for directory in os.listdir(DATABASE_ROOT):
    try:
        int(directory)  # Upewnij się że wchodzimy tylko do katalogów, których nazwy to liczby
    except:
        continue
    x = open(DATABASE_ROOT+'/'+directory+'/ONLINE','w')
    x.write("0")
    del x
exit(0)