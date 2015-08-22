class P24Order(object):
    def supply_id(self, id):
        '''Supplies with device ID for incoming consumer'''
        self.id = id
        return self

class P24ReadOrder(P24Order):
    def __init__(self, regtype, dev, port, roe=2):
        self.regtype = regtype
        self.dev = dev
        self.port = port
        self.roe = roe
        
class P24WriteOrder(P24Order):        
    def __init__(self, regtype, dev, port, val, roe=2):
        self.regtype = regtype
        self.dev = dev
        self.port = port
        self.val = val
        self.roe = roe

class P24NetinfoGetOrder(P24Order):
    pass

class P24NetinfoSetOrder(P24Order):
    def __init__(self, iptuple, subnettuple, routertuple, dnstuple, target):
        self.iptuple = iptuple
        self.subnettuple = subnettuple
        self.routertuple = routertuple
        self.dnstuple = dnstuple
        self.target = target
    
class P24KeepaliveOrder(P24Order):
    pass

class P24RebootOrder(P24Order):
    pass

class P24SleepOrder(P24Order):
    def __init__(self, seconds):
        self.seconds = seconds
        
class P24VendorinfoGetOrder(P24Order):
    pass