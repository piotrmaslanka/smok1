from thread import start_new_thread
from SocketServer import TCPServer, ThreadingMixIn
from Server.P24.RequestHandler import P24Handler
from time import sleep

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass

def launch():
    while True:
        try:
            tcs = ThreadingTCPServer(('',2405), P24Handler)
            tcs.serve_forever()
        except Exception, e :
            try:
                del tcs
            except UnboundLocalError:
                pass
        sleep(10)        # don't spam too much
        # Prevent lifecycle exceptions
    
def launch_demonize():
    start_new_thread(launch, ())
