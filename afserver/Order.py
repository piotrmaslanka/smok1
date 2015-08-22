class Order(object):
    def __init__(self, roes, transaction=None):
        object.__init__(self)
        self.roes = roes
        self.transaction = transaction
    def supplyId(self, id):
        self.id = id
        return self

class ReadOrder(Order):
    def __init__(self, address, regtype, register, roes=3, transaction=None):
        Order.__init__(self, roes, transaction)
        self.address = address
        self.regtype = regtype
        self.register = register

class WriteOrder(Order):
    def __init__(self, address, regtype, register, value, roes=3, transaction=None):
        Order.__init__(self, roes, transaction)
        self.address = address
        self.regtype = regtype
        self.register = register
        self.value = value

class NetinfoGetOrder(Order):
    def __init__(self, transaction=None):
        Order.__init__(self, 0, transaction)

class NetinfoSetOrder(Order):
    def __init__(self, iptuple, subnettuple, routertuple, dnstuple, target, transaction=None):
        Order.__init__(self, 0, transaction)
        self.iptuple = iptuple
        self.subnettuple = subnettuple
        self.routertuple = routertuple
        self.dnstuple = dnstuple
        self.target = target

class KeepaliveOrder(Order):
    def __init__(self, transaction=None):
        Order.__init__(self, 0, transaction)

class RebootOrder(Order):
    def __init__(self, transaction=None):
        Order.__init__(self, 0, transaction)

class SleepOrder(Order):
    def __init__(self, seconds):
        Order.__init__(self, 0)
        self.seconds = seconds