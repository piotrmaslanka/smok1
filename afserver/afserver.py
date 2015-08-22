#! /usr/bin/python
# coding=UTF-8
from afruntime.server import daemonize, donothing, launch

daemonize()

from CommandInterface import run as lancerorun
print 'Starting LANCERO'
launch(lancerorun)

from Server import run as p24run
print 'Starting P24'
launch(p24run)

donothing()