# coding=UTF-8
from Settings import DATABASE_ROOT
import os.path as path
from datetime import datetime
import os
# Etatowy zapisywacz do plików bazy danych p24server
def writeRunlevel(id, rlevel):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    file = open(DATABASE_ROOT+'/'+str(id)+'/RUNLEVEL', "w")
    file.write(str(rlevel))
    del file

def writeQueue(id, queue):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    file = open(DATABASE_ROOT+'/'+str(id)+'/STATS.QUEUE', "w")
    file.write(str(queue))
    del file

def getError(id):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    file = open(DATABASE_ROOT+'/'+str(id)+'/STATS.ERRORS', "r")
    return int(file.read())

def writeError(id, error):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    file = open(DATABASE_ROOT+'/'+str(id)+'/STATS.ERRORS', "w")
    file.write(str(error))
    del file

def makeOnline(id):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    file = open(DATABASE_ROOT+'/'+str(id)+'/ONLINE', "w")
    file.write("1")
    del file
def makeOffline(id):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    file = open(DATABASE_ROOT+'/'+str(id)+'/ONLINE', "w")
    file.write("0")
    del file

def writeReg(file, value):
    if value[0] == False:
        file.write("ERROR")
    else:
        if value[1] > 32767:
            file.write('-')
        file.write(str(value[1] & 32767))

def writeInput(file, value):
    if value[0] == False:
        file.write("ERROR")
    else:
        file.write(str(value[1]))

def writeFlag(file, value):
    if value[0] == False:
        file.write("ERROR")
    else:
        if value[1]:
            file.write("1")
        else:
            file.write("0")
        
def write(id, dev, regtype, register, value):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass
    
    if regtype == 0:
        regtype = 'r'
    elif regtype == 1:
        regtype = 'f'
    elif regtype == 2:
        regtype = 'i'
        
    file = open(DATABASE_ROOT+'/'+str(id)+'/'+str(dev)+regtype+str(register), "w")     

    if regtype == 'r':
        writeReg(file, value)
    elif regtype == 'f':
        writeFlag(file, value)
    elif regtype == 'i':
        writeInput(file, value)
    del file
        
def writeVendorInfo(id, strin):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass        # Directory exists
    file = open(DATABASE_ROOT+'/'+str(id)+'/NETWORK', "w")        
    file.write(strin)
    del file
        
def writeSettings(id, settings):
    try:
        os.mkdir(DATABASE_ROOT+'/'+str(id))
    except:
        pass        # Directory exists
    file = open(DATABASE_ROOT+'/'+str(id)+'/NETWORK', "w")        
    file.write(str(settings[0][0])+'.'+str(settings[0][1])+'.'+str(settings[0][2])+'.'+str(settings[0][3])+"\n")    
    file.write(str(settings[1][0])+'.'+str(settings[1][1])+'.'+str(settings[1][2])+'.'+str(settings[1][3])+"\n")    
    file.write(str(settings[2][0])+'.'+str(settings[2][1])+'.'+str(settings[2][2])+'.'+str(settings[2][3])+"\n")    
    file.write(str(settings[3][0])+'.'+str(settings[3][1])+'.'+str(settings[3][2])+'.'+str(settings[3][3])+"\n")
    file.write(settings[4])
    del file    
    