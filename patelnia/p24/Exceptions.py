class P24Exception(Exception):
    pass

class DeviceNotExist(P24Exception):
    '''Device of given devid is not registered within the database'''
    def __init__(self, devid):
        self.devid = devid
    def __str__(self):
        return 'Device ID='+str(self.devid)+' is not registered'
    
class DeviceOffline(P24Exception):
    '''Device is offline'''

class InterfaceError(P24Exception):
    '''Module used wrongly'''
    def __init__(self, kmsg):
        self.kmsg = kmsg
    def __str__(self):
        return self.kmsg
    
class Readonly(InterfaceError):
    '''Property is read-only'''    
    
class ReadFailed(P24Exception):
    '''Failed to read'''
    def __str__(self):
        return 'Read has failed'    
    
class NotReaded(ReadFailed):
    '''Value has not yet been readed'''
    def __str__(self):
        return 'Requested data has not yet been readed'
    
class ReadErrored(ReadFailed):
    '''Remote device returned an ERROR on read order'''
    def __str__(self):
        return 'The device has returned an error'
    
class DatabaseFailure(P24Exception):
    def __str__(self):
        return 'Encountered database error'    
class InvalidData(P24Exception):
    '''Invalid data has been passed to function'''
    def __init__(self, s):
        self.s = self
    def __str__(self):
        return self.s

class RegistryError(P24Exception):
    def __str__(self):
        return 'Encountered registry error'    
        
class EntryNotExist(RegistryError):
    '''Registry entry does not exist'''
    def __init__(self, s):
        self.s = s
    def __str__(self):
        return 'Registry entry "'+str(self.s)+'" does not exist'
    
class UpdatedNotReady(P24Exception):
    def __str__(self):
        return 'Updated operation not ready'''    
    