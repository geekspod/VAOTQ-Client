import time
from dronekit import connect, VehicleMode

from utils.Log import Log


class Controller:
    def __init__(self, port='/dev/ttyACM0', baud=921600):
        self.log = Log(type(self).__name__)
        self.vehicle = None
        self.log.info("Connecting to vehicle")
        self.connect_to_vehicle(port, baud)
        self.log.info("Connected to Vehicle")

        self.log.info("Setting vehicle mode to GUIDED_NOGPS")
        self.set_vehicle_mode('GUIDED_NOGPS')
        self.log.info("Mode set")

        self.log.info("Testing vehicle")
        self.check()
        self.log.info("Test complete")

    def connect_to_vehicle(self, port, baud):
        self.vehicle = connect(port, baud, wait_ready=True)

    def set_vehicle_mode(self, mode):
        self.vehicle.mode = VehicleMode(mode)

    def arm(self):
        self.vehicle.arm(wait=True)

    def disarm(self):
        self.vehicle.disarm(wait=True)

    def check(self):
        self.arm()
        time.sleep(5)
        self.disarm()

    @staticmethod
    def is_valid_command(command):
        return command in ['arm', 'disarm']

    def handle_command(self, command):
        if command == 'arm':
            self.arm()
        elif command == 'disarm':
            self.disarm()
        else:
            print("Invalid command")
