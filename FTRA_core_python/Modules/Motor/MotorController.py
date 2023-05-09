import serial

class MotorController:
    def __init__(self, port, baudrate, pastValue = [90, 90, 90, 90, 90, 90]):
        self.py_serial = serial.Serial(
            port = port,
            baudrate = baudrate
        )
        self.pastValue = pastValue

    def arrToString(self, command):
        ret = ' '.join(map(str,command))
        return ret 

    def checkDiff(self, command):
        for i in range(6):
            if abs(self.pastValue[i] - command[i]) < 10:
                command[i] = self.pastValue[i]
        return command
    
    def setMotor(self, command):
        ret = self.checkDiff(command.tolist())
        ret = self.arrToString(ret)
        self.pastValue = ret
        self.py_serial.write(ret.encode())
        
    