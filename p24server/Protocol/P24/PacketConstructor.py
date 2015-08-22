# coding=UTF-8
def getI_INITIALIZATION_1(BasePacket):
    BasePacket.resetPointer()
    Identifier = (BasePacket.getDword() << 32) + BasePacket.getDword()
    ProtoVersion = BasePacket.getDword()
    return (Identifier, ProtoVersion)
    
def mkCONFIRMATION(BasePacket):
    BasePacket.reset()
    BasePacket.addByte(0)
    
def mkLOGINREFUSAL(BasePacket):
    BasePacket.reset()
    BasePacket.addByte(254)    
    
def mkGIVE_ME_SETTINGS(BasePacket):
    BasePacket.reset()
    BasePacket.addByte(2)
    
def mkWRITE_COIL(BasePacket, Device, Register, Value):    
    BasePacket.reset()
    BasePacket.addByte(6)
    BasePacket.addWord(Register)
    if Value:
        BasePacket.addByte(1)
    else:
        BasePacket.addByte(0)
    BasePacket.addByte(Device)
    
def mkKEEPALIVE(BasePacket):
    BasePacket.reset()
    BasePacket.addByte(0)
    
def getKEEPALIVE(BasePacket):
    BasePacket.resetPointer()    
    if BasePacket.getByte() == 0:
        return (True, )
    else:
        return (False, )
    
def getGET_COIL_RET_ERROR(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, BasePacket.getByte() == 1)
    else:
        return (False, BasePacket.getByte())
def mkGET_NETWORK_CLIENT_VENDOR(BasePacket):
    BasePacket.reset()
    BasePacket.addByte(7)

def getGET_NETWORK_CLIENT_VENDOR(BasePacket):
    BasePacket.resetPointer()
    BasePacket.getByte()
    return (BasePacket.getString(), )
        
        
def mkWRITE_HOLDING(BasePacket, Device, Register, Value):
    BasePacket.reset()
    BasePacket.addByte(5)
    BasePacket.addWord(Register)
    BasePacket.addWord(Value)
    BasePacket.addByte(Device)


def getWRITE_GENERIC(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, )
    else:
        return (False, BasePacket.getByte())

def getWRITE_HOLDING(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, )
    else:
        return (False, BasePacket.getByte())
def getWRITE_COIL(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, )
    else:
        return (False, BasePacket.getByte())

def getCOIL_HOLDING(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, )
    else:
        return (False, BasePacket.getByte())


def mkGET_COIL_RET_ERROR(BasePacket, Device, Register):    
    BasePacket.reset()
    BasePacket.addByte(4)
    BasePacket.addWord(Register)
    BasePacket.addByte(Device)
    
def mkGET_HOLDING_RET_ERROR(BasePacket, Device, Register):
    BasePacket.reset()
    BasePacket.addByte(3)
    BasePacket.addWord(Register)
    BasePacket.addByte(Device)
    
def getGET_HOLDING_RET_ERROR(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, BasePacket.getWord())
    else:
        return (False, BasePacket.getByte())
    
def mkGET_INPUT_RET_ERROR(BasePacket, Device, Register):
    BasePacket.reset()
    BasePacket.addByte(8)
    BasePacket.addWord(Register)
    BasePacket.addByte(Device)
    
def getGET_INPUT_RET_ERROR(BasePacket):
    BasePacket.resetPointer()
    if BasePacket.getByte() == 0:
        return (True, BasePacket.getWord())
    else:
        return (False, BasePacket.getByte())

def mkCOMPLEX_SETTINGS_PRZEPIER(BasePacket, conftuple):
    '''Config tuple is a tuple of:
        tuple - 4 integers, making desired IP
        tuple - 4 integers, making desired subnet
        tuple - 4 integers, making desired gateway
        tuple - 4 integers, making desired DNS
        string - making desired hostname'''
    BasePacket.reset()
    BasePacket.addByte(1)
    BasePacket.addByte(conftuple[0][0])
    BasePacket.addByte(conftuple[0][1])
    BasePacket.addByte(conftuple[0][2])
    BasePacket.addByte(conftuple[0][3])
    
    BasePacket.addByte(conftuple[1][0])
    BasePacket.addByte(conftuple[1][1])
    BasePacket.addByte(conftuple[1][2])
    BasePacket.addByte(conftuple[1][3])
    
    BasePacket.addByte(conftuple[2][0])
    BasePacket.addByte(conftuple[2][1])
    BasePacket.addByte(conftuple[2][2])
    BasePacket.addByte(conftuple[2][3])
    
    BasePacket.addByte(conftuple[3][0])
    BasePacket.addByte(conftuple[3][1])
    BasePacket.addByte(conftuple[3][2])
    BasePacket.addByte(conftuple[3][3])
    
    BasePacket.addString(conftuple[4])
    
def mkGETVENDORINFO(BasePacket):
    BasePacket.resetPointer()
    BasePacket.addByte(7)
    
def getGETVENDORINFO(BasePacket):
    BasePacket.resetPointer()
    BasePacket.getByte()
    return BasePacket.getString()
    
def getGIVE_ME_SETTINGS(BasePacket):
    BasePacket.resetPointer()
    BasePacket.getByte()
    ip1 = BasePacket.getByte()
    ip2 = BasePacket.getByte()
    ip3 = BasePacket.getByte()
    ip4 = BasePacket.getByte()
    sn1 = BasePacket.getByte()
    sn2 = BasePacket.getByte()
    sn3 = BasePacket.getByte()
    sn4 = BasePacket.getByte()
    gw1 = BasePacket.getByte()
    gw2 = BasePacket.getByte()
    gw3 = BasePacket.getByte()
    gw4 = BasePacket.getByte()
    dn1 = BasePacket.getByte()
    dn2 = BasePacket.getByte()
    dn3 = BasePacket.getByte()
    dn4 = BasePacket.getByte()
    target = BasePacket.getString()
    return ((ip1,ip2,ip3,ip4), (sn1,sn2,sn3,sn4), (gw1,gw2,gw3,gw4), (dn1,dn2,dn3,dn4), target)    