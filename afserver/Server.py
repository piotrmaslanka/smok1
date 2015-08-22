# coding=UTF-8
from afruntime.log import log as debugLog
from afruntime.Exceptions import StatisticNotFound, DeviceNotFound
from datetime import datetime, timedelta
from afruntime.device import Device
from afruntime.device.classes import ERR_SUCCESS
import SocketServer
from Protocol import *
from socket import SOL_TCP, TCP_NODELAY, SOL_SOCKET, SO_KEEPALIVE
import Queue
from time import sleep
from weakref import proxy
from Order import *
from Connections import CONNECTIONS
from threading import Thread
from lancero.operators import Get
import lancero.client
import lancero.base
from afruntime.config import getRegistry

lancero.client.registerServer(lancero.client.ServerDefinitionEntry('127.0.0.1', getRegistry('afsensors-lancero-port'), 'afsensors', ''))
afsObj = lancero.base.RemoteProxy(lancero.base.RemoteSource('afsensors', 0))


class ReaderThread(Thread):
    def __init__(self, rqh):
        '''I assume RQH is a WeakProxy'''
        self.rqh = rqh
        self.device = rqh.device
        self.device.setStat('thread.reader', 1)
        self.id = rqh.id
        Thread.__init__(self)

    def run(self):
        try:
            self.xrun()
        except Exception, e:
            self.device.setStat('thread.reader', 0)
            self.device.setStat('online', 0)
            Get(afsObj.offline(self.id))
            try:
                del CONNECTIONS[self.id]
            except:
                pass
            debugLog('reader exception for '+str(self.id)+': '+str(e))

  
    def xrun(self):
        self.device.setStat('thread.reader.lasttick', datetime.now())
        self.device.setStat('thread.reader.status', 'start')
        packa = RequestHandlerPacket(self.rqh)
        while True:
           self.device.setStat('queue.sent', self.rqh.incoming.qsize())
           self.device.setStat('thread.reader.status', 'wait')
           order = self.rqh.incoming.get(True, 61) # czekaj na następny rozkaz
           self.device.setStat('thread.reader.status', 'readin')

           packa.readIn()
           self.device.setStat('thread.reader.status', 'readedin')
           self.device.setStat('thread.reader.lasttick', datetime.now())
           if isinstance(order, ReadOrder):
                rti = [getGET_HOLDING_RET_ERROR, getGET_COIL_RET_ERROR, getGET_INPUT_RET_ERROR]
                pr = rti[order.regtype](packa)

                if pr.error != ERR_SUCCESS:
                    self.device.setStat('transmission.errors', self.device.getStat('transmission.errors')+1)

                    if self.device.getRegistry('correct.errors'):
                        order.roes -= 1
                        if order.roes <= 0:
                            self.device.setValue(order.address, order.regtype, order.register, pr)
                        else:
                            self.rqh.orders.put(order)
                    else:
                        self.device.setValue(order.address, order.regtype, order.register, pr)
                else:
                    self.device.setStat('transmission.successes', self.device.getStat('transmission.successes')+1)
                    if order.transaction != None:
                        self.device.setTransaction(order.transaction)
                    self.device.setValue(order.address, order.regtype, order.register, pr)
           if isinstance(order, WriteOrder):
                if getWRITE_GENERIC(packa):
                    self.device.setStat('transmission.successes', self.device.getStat('transmission.successes')+1)
                    if order.transaction != None:
                        self.device.setTransaction(order.transaction)                    
                else:
                    self.device.setStat('transmission.errors', self.device.getStat('transmission.errors')+1)
                    if self.device.getRegistry('correct.errors'):
                        order.roes -= 1
                        if order.roes > 0:
                            self.rqh.orders.put(order)
           if isinstance(order, NetinfoGetOrder):
                ntfo = getGIVE_ME_SETTINGS(packa)
                writeSettings(order.id, ntfo)
           if isinstance(order, NetinfoSetOrder):
                self.device.setStat('transmission.successes', self.device.getStat('transmission.successes')+1)
                if order.transaction != None:
                    self.device.setTransaction(order.transaction)
           if isinstance(order, KeepaliveOrder):
                self.device.setStat('transmission.successes', self.device.getStat('transmission.successes')+1)
                if order.transaction != None:
                    self.device.setTransaction(order.transaction)


class P24Handler(SocketServer.BaseRequestHandler):    # Obiekty przetwarzający, yay!
    def finish(self):
        self.device.setStat('thread.handler', 0)
        self.device.setStat('online', 0)
        self.device.setStat('disconnected.on', datetime.now())
        try:
            Get(afsObj.offline(self.id))
        except:
            pass
        debugLog('Finishing for '+str(self.id))
        try:
            del CONNECTIONS[self.id]
        except:
            pass

    def stall_incoming(self):
        self.device.setStat('thread.handler.status', 'stall')
        self.device.setStat('queue.pending', self.orders.qsize())

        if self.device.getStat('thread.reader.lasttick') + timedelta(0, 60) < datetime.now():
            debugLog('Handler quits due to thread.reader watchdog faulting')
            self.device.setStat('thread.reader.lasttick.watchdogged', datetime.now())
            raise Exception, ' watchdog'

        while self.incoming.qsize() > 100:
            self.device.setStat('thread.handler.status', 'stall-busywait')
            if self.device.getStat('thread.reader.lasttick') + timedelta(0, 60) < datetime.now():
                debugLog('Handler quits due to thread.reader watchdog faulting')
                self.device.setStat('thread.reader.lasttick.watchdogged', datetime.now())
                raise Exception, 'qsize > 100 + watchdog'
            sleep(1)

    def handle(self):
        '''If an exception happens in handle(), then finish() is not executed'''
        self.request.setsockopt(SOL_TCP, TCP_NODELAY, 1) # Nagle - sio!
        self.request.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 0) # no keepalive
        self.request.setblocking(1)
        self.request.settimeout(60)
        self.packet = RequestHandlerPacket(proxy(self))
        self.packet.readInStrict(12) # wczytaj pakiet inicjalizacji
        id, self.protocolVersion = getI_INITIALIZATION(self.packet)

        debugLog('Remote identified as '+str(id))

        self.id = id
        self.incoming = Queue.Queue()
        self.orders = Queue.Queue()

        try:
            self.device = Device(id)
        except DeviceNotFound:
            debugLog('Unrecognized device '+str(id))
            return

        try:
            if self.device.getStat('thread.handler') == 1:
                raise Exception
            if self.device.getStat('thread.reader') == 1:
                raise Exception
        except StatisticNotFound:
            pass

        CONNECTIONS[self.id] = self

        try:
            self.xhandle()
        except Exception, e:
            debugLog('Exception for '+str(self.id)+': '+str(e))
            
            
    def xhandle(self):
            # Przygotuj statystyki
        self.device.setStat('thread.handler', 1)
        self.device.setStat('transmission.errors', 0)
        self.device.setStat('transmission.successes', 0)
        self.device.setStat('queue.sent', 0)
        self.device.setStat('queue.pending', 0)
        self.device.setStat('connected.on', datetime.now())
        self.device.setStat('online', 1)
        self.device.setStat('last.tick', None)

        Get(afsObj.online(self.id))
        self.device.setStat('thread.handler.status', 'start')

        rant = ReaderThread(proxy(self))
        rant.start()
        mkCONFIRMATION(self.packet)
        self.packet.writeOut()
        debugLog('Passing onto main loop for '+str(self.id))
        while True:
            self.device.setStat('thread.handler.status', 'WAIT')
            try:
                order = self.orders.get(True, 61) # czekaj na następny rozkaz
            except:
                debugLog('Disconnected '+str(self.id)+' because of no orders')
                raise Exception, 'no orders'

            if isinstance(order, ReadOrder):
                self.stall_incoming()
                rti = [mkGET_HOLDING_RET_ERROR, mkGET_COIL_RET_ERROR, mkGET_INPUT_RET_ERROR]
                rti[order.regtype](self.packet, order.address, order.register)
                self.packet.writeOut()
                self.incoming.put(order.supplyId(self.id))
            elif isinstance(order, WriteOrder):
                self.stall_incoming()
                rti = [mkWRITE_HOLDING, mkWRITE_COIL]
                rti[order.regtype](self.packet, order.address, order.register, order.value)
                self.packet.writeOut()
                self.incoming.put(order.supplyId(self.id))
                debugLog('sent write')
            elif isinstance(order, NetinfoGetOrder):
                self.stall_incoming()
                mkGIVE_ME_SETTINGS(self.packet)
                self.packet.writeOut()
                self.incoming.put(order.supplyId(self.id))
            elif isinstance(order, NetinfoSetOrder):
                self.stall_incoming()
                mkCOMPLEX_SETTINGS_PRZEPIER(self.packet, (order.iptuple, order.subnettuple, order.routertuple, order.dnstuple, order.target))
                self.packet.writeOut()
                self.incoming.put(order.supplyId(self.id))
            elif isinstance(order, KeepaliveOrder):
                self.stall_incoming()
                mkKEEPALIVE(self.packet)
                self.packet.writeOut()
                self.incoming.put(order.supplyId(self.id))
            elif isinstance(order, RebootOrder):  # Jak najprościej zrobić reboota? Rozłączyć urządzenie.
                return
            elif isinstance(order, SleepOrder):
                sleep(order.seconds)
            elif isinstance(order, VendorinfoGetOrder):
                self.stall_incoming()
                mkGETVENDORINFO(self.packet)
                self.packet.writeOut()
                self.incoming.put(order.supplyId(self.id))
            self.device.setStat('last.tick', datetime.now())

from afruntime.server import donothing
from SocketServer import ThreadingMixIn, TCPServer


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass

def run():
    tcs = ThreadingTCPServer(('', getRegistry('afserver-p24-port')), P24Handler)
    tcs.serve_forever()
    print 'P24 started'
    donothing()
    
