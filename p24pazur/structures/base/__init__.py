from patelnia.scripts.Application import Application, Sensor
from datetime import timedelta
from common import DateTimeSyncer

class MyApplication(Application):
        # Define sensors here
    hour = Sensor(1, 0, 4002)
    minute = Sensor(1, 0, 4001)

    def init(self):
        self.apps.append(DateTimeSyncer(self, timedelta(1), self.hour, self.minute))