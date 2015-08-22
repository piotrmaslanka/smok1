from patelnia.p24.Settings import P24DATABASE_ROOT
import datetime
import codecs

class Notification(object):
    def __init__(self, date, info, code, severity=None):
        self.date = date
        self.code = code
        self.info = info
        self.severity = severity
    def __unicode__(self):
        return unicode(self.severity)+u'|'+unicode(self.date.__repr__())+u'|'+unicode(self.code)+u'|'+unicode(self.info)

class Alarm(Notification):
    def __init__(self, date, info, code): Notification.__init__(self, date, info, code, 0)
    def __str__(self): return Notification.__str__(self)
class Alert(Notification):
    def __init__(self, date, info, code): Notification.__init__(self, date, info, code, 1)
    def __str__(self): return Notification.__str__(self)
class Notice(Notification):
    def __init__(self, date, info, code): Notification.__init__(self, date, info, code, 2)
    def __str__(self): return Notification.__str__(self)

def mkAlarm(info, code):
    return Alarm(datetime.datetime.now(), info, code)
def mkAlert(info, code):
    return Alert(datetime.datetime.now(), info, code)
def mkNotice(info, code):
    return Notice(datetime.datetime.now(), info, code)

class AlertRegistry(object):
    def __len__(self):
        if not self.fileloaded:
            self.loadDict()
        return len(self.flist)
    def __iter__(self):
        if not self.fileloaded:
            self.loadDict()
        return self.flist.__iter__()
    def loadDict(self):
        try:
            f = codecs.open(P24DATABASE_ROOT+str(self.devid)+'/REGISTRY/LOG.ALERT', 'r', encoding='utf-8')
        except:
            self.flist = self.appends
            self.fileloaded = True
            return
        mylist = []
        for line in f.readlines():
            data = line.split('|')
            date = eval(data[1]) 
            level = int(data[0])
            if level == 0:
                mylist.append(Alarm(date, data[3], data[2]))
            elif level == 1:
                mylist.append(Alert(date, data[3], data[2]))
            elif level == 2:
                mylist.append(Notice(date, data[3], data[2]))
        mylist = mylist + self.appends
        self.fileloaded = True
        self.flist = mylist
    def append(self, msgObj):
        if self.fileloaded:
            self.flist.append(msgObj)
        else:
            self.appends.append(msgObj)
    def save(self):
        if not self.fileloaded:
            if self.appends != []:
                try:
                    f = codecs.open(P24DATABASE_ROOT+str(self.devid)+'/REGISTRY/LOG.ALERT','a',encoding='utf-8')
                except:
                    f = codecs.open(P24DATABASE_ROOT+str(self.devid)+'/REGISTRY/LOG.ALERT','w',encoding='utf-8')
                for i in self.appends:
                    f.write(unicode(i)+u'\n')
                self.appends = []
        else:
            f = codecs.open(P24DATABASE_ROOT+str(self.devid)+'/REGISTRY/LOG.ALERT','w',encoding='utf-8')
            for i in self.flist:
                f.write(unicode(i)+u'\n')
    def __init__(self, devid):
        self.devid = devid
        self.fileloaded = False
        self.appends = []
    def __getitem__(self, key):
        if not self.fileloaded:
            self.loadDict()
        return self.flist[key]
    def __setitem__(self, key, val):
        if not self.fileloaded:
            self.loadDict()
        self.flist[key] = val
    def __delitem__(self, key):
        if not self.fileloaded:
            self.loadDict()
        del self.flist[key]
        
def fastAlertAppend(id, alertobject):
    x = AlertRegistry(id)
    x.append(alertobject)
    x.save()
        