#! /usr/bin/python
# coding=UTF-8
from afruntime.server import daemonize, donothing, launch

daemonize()

from CommandInterface import run as lancerorun
print 'Starting LANCERO'
launch(lancerorun)

from Sensorics import run as sensoricsrun
print 'Starting Sensorics'
launch(sensoricsrun)

donothing()