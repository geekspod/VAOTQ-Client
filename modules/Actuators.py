from utils.Log import Log
from utils.constants import THRESH_DISTANCE


class Actuators:
    def __init__(self):
        self.command = None
        self.log = Log(type(self).__name__)

    def set_command(self, command):
        if self.command != command:
            self.log.info("New coordinates {0}, command: {1}".format(command, self.get_actuator_command()))
        self.command = command

    def get_actuator_command(self):
        angle = self.command['angle']
        distance = self.command['distance']

        if distance < THRESH_DISTANCE:
            return None
        else:
            if 0 <= angle <= 90:
                return 'topleft'
            elif 90 < angle <= 180:
                return 'topright'
            elif 180 < angle <= 270:
                return 'bottomright'
            elif 270 < angle <= 360:
                return 'bottomleft'
            else:
                return None
