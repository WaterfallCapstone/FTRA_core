import serial

class MotorController:
    def __init__(self, port, baudrate):
        self.py_serial = serial.Serial(
            port = port,
            baudrate = baudrate
        )

    def arrToString(self, command):
        ret = ' '.join(command)
        return ret

    def setMotor(self, command):
        ret = self.arrToString(command)
        self.py_serial.write(ret.encode())
        
    