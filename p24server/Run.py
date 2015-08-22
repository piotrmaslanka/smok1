# coding=UTF-8
import Sensorics
import Server
import CommandInterface

def launch():
    Sensorics.launch_demonize()
    Server.P24.launch_demonize()
    CommandInterface.launch_demonize()