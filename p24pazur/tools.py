import halonet

def sms(msg):
    w = halonet.HalonetWebsite()
    w.login('fixed0577','2405199100')
    w.sms('+48783884334','SMOK',msg,'1de02e25486f63eaca09d8260c791da0')
