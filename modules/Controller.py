import time

from dronekit import connect, VehicleMode


class Controller:
    def __init__(self, port='/dev/ttyACM0', baud=921600):
        self.vehicle = None
        self.connect_to_vehicle(port, baud)
        self.set_vehicle_mode('GUIDED_NOGPS')
        self.check()

    def connect_to_vehicle(self, port, baud):
        self.vehicle = connect(port, baud)

    def set_vehicle_mode(self, mode):
        self.vehicle.mode = VehicleMode(mode)

    def arm(self):
        self.vehicle.arm()

    def disarm(self):
        self.vehicle.disarm()

    def check(self):
        if self.vehicle.is_armable:
            self.arm()
            time.sleep(1)
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
