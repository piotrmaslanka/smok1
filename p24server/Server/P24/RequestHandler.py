# coding=UTF-8
import SocketServer
from Protocol.Packet import RequestHandlerPacket
from Protocol.P24.PacketConstructor import *
from socket import SOL_TCP, TCP_NODELAY, SHUT_RDWR
from datetime import datetime
from Server.P24.FileWriter import *
from Server.P24.Orders import *
import Queue
from time import sleep
from weakref import proxy
from patelnia.p24.Alert import mkNotice, fastAlertAppend

from Server.Connections import CONNECTIONS
from threading import Thread

class ReaderThread(Thread):
    def __init__(self, rqh):
        '''I assume RQH is a WeakProxy'''
        self.rqh = rqh
        Thread.__init__(self)
    def run(self):
        packa = RequestHandlerPacket(self.rqh)
        while True:
           try:
                order = self.rqh.incoming.get(True, 61) # czekaj na następny rozkaz
           except Queue.Empty:
                return
            
           packa.readIn()
            
           if isinstance(order, P24ReadOrder):
                if order.regtype == 0:
                    pr = getGET_HOLDING_RET_ERROR(packa)
                if order.regtype == 1:
                    pr = getGET_COIL_RET_ERROR(packa)
                if order.regtype == 2:
                    pr = getGET_INPUT_RET_ERROR(packa)

                if pr[0] == False:
                    err = getError(self.rqh.id)
                    writeError(self.rqh.id, err+1)
                    if (order.roe > 0) and (err < 11):
                       order.roe -= 1
                       self.rqh.orders.put(order)

                write(order.id, order.dev, order.regtype, order.port, pr)
           if isinstance(order, P24WriteOrder):
                pr = getWRITE_GENERIC(packa)
                if pr[0] == False:
                    err = getError(self.rqh.id)
                    writeError(self.rqh.id, err+1)
                    if (order.roe > 0) and (err < 11):
                       order.roe -= 1
                       self.rqh.orders.put(order)

           if isinstance(order, P24NetinfoGetOrder):
                ntfo = getGIVE_ME_SETTINGS(packa)
                writeSettings(order.id, ntfo)
           if isinstance(order, P24NetinfoSetOrder):
                pass
           if isinstance(order, P24KeepaliveOrder):
                pass
           if isinstance(order, P24VendorinfoGetOrder):
                vinf = getGETVENDORINFO(packa)
                writeVendorInfo(order.id, vinf)
            

class P24Handler(SocketServer.BaseRequestHandler):    # Obiekty przetwarzający, yay!
    def finish(self):
        from Sensorics import clearSensorsFor
        try:
            makeOffline(self.id) # odpisz bycie online
            clearSensorsFor(self.id)
        except:
            pass
        try:
            del CONNECTIONS[self.id]
        except:
            pass
    def handle(self):
        '''If an exception happens in handle(), then finish() is not executed'''
        self.graceful = False
        try:
            self.xhandle()
        except Exception, e:
            try:
                self.id
            except:
                pass
            else:
                if not self.graceful:
                    if str(e)=='timed out':
                        fastAlertAppend(self.id, mkNotice(u'Rozłączony: zanik połączenia','disconnected:timeout'))
                    else:
                        fastAlertAppend(self.id, mkNotice(u'Rozłączony: wyjątek '+str(e),'disconnected:exception:'+str(e)))
        
    def stall_incoming(self):   
        '''Prevents device buffer overflow'''
        while self.incoming.qsize() > 100:
            sleep(1)    
        
    def xhandle(self):
        from Sensorics import readSensorsFor
        self.runlevel = 0   # domyślny runlevel
        self.request.setsockopt(SOL_TCP, TCP_NODELAY, 1) # Nagle - sio!
        self.request.setblocking(1)
        self.request.settimeout(20)
        self.packet = RequestHandlerPacket(proxy(self)) # stwórz obiekt pakietowy
        self.orders = Queue.Queue() # rozkazy to pusta kolejka
        self.packet.readInStrict(12) # wczytaj pakiet inicjalizacji
        id, self.protocolVersion = getI_INITIALIZATION_1(self.packet) 

        try:
            CONNECTIONS[id]
        except:
            pass
        else:
            self.graceful = True
            mkLOGINREFUSAL(self.packet)
            self.packet.writeOut()
            return
        
        self.id = id
        writeError(id, 0)
        fastAlertAppend(id, mkNotice(u'Polaczono z '+str(self.client_address), u'connected'))
        self.incoming = Queue.Queue()
        rant = ReaderThread(proxy(self))
        rant.start()
        CONNECTIONS[self.id] = self
        makeOnline(self.id) # zapisz bycie online
        readSensorsFor(self.id)
        mkCONFIRMATION(self.packet)
        self.packet.writeOut()
        self.lastSentPacket = datetime.now()
        while True:
            try:
                order = self.orders.get(True, 61) # czekaj na następny rozkaz
            except Queue.Empty:
                fastAlertAppend(self.id, mkNotice(u'Rozlaczono z braku rozkazów', u'disconnected:lack_of_orders'))
                self.graceful = True
                return

            writeQueue(self.id, len(self.orders.qsize()))

            if self.runlevel == 1:
                if (datetime.now() - self.rlvl1lastreported).seconds > 15:
                    from Sensorics import umfastRead
                    umfastRead(self.id)
            
            self.lastSentPacket = datetime.now() # ostatni pakiet wysłano TERAZ - to dla keepalive, kiedyś się przyda
            if isinstance(order, P24ReadOrder):
                self.stall_incoming()
                if order.regtype == 0:
                    mkGET_HOLDING_RET_ERROR(self.packet, order.dev, order.port)
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
                elif order.regtype == 1:
                    mkGET_COIL_RET_ERROR(self.packet, order.dev, order.port)
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
                elif order.regtype == 2:
                    mkGET_INPUT_RET_ERROR(self.packet, order.dev, order.port)
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
            elif isinstance(order, P24WriteOrder):
                self.stall_incoming()
                if order.regtype == 0:
                    mkWRITE_HOLDING(self.packet, order.dev, order.port, order.val)
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
                elif order.regtype == 1:
                    mkWRITE_COIL(self.packet,order.dev, order.port, order.val)
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
            elif isinstance(order, P24NetinfoGetOrder):
                    self.stall_incoming()                
                    mkGIVE_ME_SETTINGS(self.packet)
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
            elif isinstance(order, P24NetinfoSetOrder):
                    self.stall_incoming()
                    mkCOMPLEX_SETTINGS_PRZEPIER(self.packet, (order.iptuple, order.subnettuple, order.routertuple, order.dnstuple, order.target))
                    self.packet.writeOut()
                    self.incoming.put(order.supply_id(self.id))
            elif isinstance(order, P24KeepaliveOrder):
                self.stall_incoming()                
                mkKEEPALIVE(self.packet)
                self.packet.writeOut()
                self.incoming.put(order.supply_id(self.id))
            elif isinstance(order, P24RebootOrder):  # Jak najprościej zrobić reboota? Rozłączyć urządzenie.
                break
            elif isinstance(order, P24SleepOrder):
                sleep(order.seconds)
            elif isinstance(order, P24VendorinfoGetOrder):
                self.stall_incoming()                
                mkGETVENDORINFO(self.packet)
                self.packet.writeOut()
                self.incoming.put(order.supply_id(self.id))