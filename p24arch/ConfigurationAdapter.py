import MySQLdb
from Settings import DB_USER, DB_PASS, DB_HOST, DB_DB

def writeReport(archid, datetime, value):
    CONNECTION = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_DB)
    cur = CONNECTION.cursor()
    cur.execute("""INSERT INTO arch_read VALUES (NULL, %s , %s , %s )""", (archid, datetime, value))

def getSensorsForDevice(device_number):
        # First, determine Device_id
    CONNECTION = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_DB)
    cur = CONNECTION.cursor()
    cur.execute("""SELECT id FROM manage_device WHERE dev_number= %s """, (device_number,))
    devid, = cur.fetchone()
    
    cur.execute("""SELECT arch_archsensor.id,
                          device_sensor.Device_id,
                          device_sensor.modbus_devid,
                          device_sensor.regtype,
                          device_sensor.register,
                          device_sensor.datatype,
                          device_sensor.interval_0 
                   FROM arch_archsensor
                   LEFT JOIN device_sensor ON arch_archsensor.Sensor_id=device_sensor.id 
                   WHERE device_sensor.Device_id= %s """, (devid, ))
    return cur.fetchall()


def getAllDevices():
    CONNECTION = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_DB)
    cur = CONNECTION.cursor()
    cur.execute('SELECT dev_number FROM manage_device')
    z = cur.fetchall()
    return z