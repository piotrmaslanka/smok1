#! /usr/bin/python
# coding=UTF-8
from Run import launch
from time import sleep
import sys
import os
import resource
from Settings import DATABASE_ROOT

        # uruchom sie jako daemon
try: 
     pid = os.fork() 
     if pid > 0:
         sys.exit(0) 
except OSError, e: 
     print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
     sys.exit(1)
os.chdir("/") 
os.setsid() 
os.umask(0)
try: 
     pid = os.fork() 
     if pid > 0:
         sys.exit(0) 
except OSError, e: 
     print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
     sys.exit(1) 


launch()        # odpal wątki
while True:
    sleep(1000)     # główny wątek się opiernicza