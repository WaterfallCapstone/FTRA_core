import serial

class MotorController:
    def __init__(self, port, baudrate, pastValue = [90, 90, 90, 90, 90, 90], stat = "control"):
        self.py_serial = serial.Serial(
            port = port,
            baudrate = baudrate
        )
        self.pastValue = pastValue
        self.stat = stat
    
    def setStat(self,stat):
        if(stat == "control" or stat == "tracking"):
            self.stat = stat

    def arrToString(self, command):
        # ret = ' '.join(map(str,command))
        ret = ' '.join(str(command))
        return ret 

    

    # def checkDiff(self, command):
    #     for i in range(6):
    #         if abs(self.pastValue[i] - command[i]) < 10:
    #             command[i] = self.pastValue[i]
    #     return command
    
    def calculate_next(self, past, dest):
        return
    
    def setMotor(self, past, dest):
        if self.stat == "tracking":
            next = self.calculate_next(past, dest)
        else:
            next = dest.tolist()
        # ret = self.arrToString(command.tolist())
        # self.pastValue = ret
        # print("motor ret " , ret)
        # self.py_serial.write(ret.encode())
        
    