#! /usr/bin/python
# coding=UTF-8
from afruntime.server import daemonize, donothing
from afruntime import DEVDB_ROOT
from thread import start_new_thread
from Handler import start
daemonize()


for line in open(DEVDB_ROOT+'motemote', 'r').readlines():
    id, ip, port = line.split(' ')
    id = int(id)
    port = int(port)
    print 'Starting mote IP='+str(ip)+' PORT='+str(port)+' ID='+str(id)
    start_new_thread(start, (id, ip, port)) 

donothing()