import serial
import serial.tools.list_ports as sp

class MotorController:
    def __init__(self, port, baudrate, pastValue = [90, 90, 90, 90, 90, 90], stat = "control"):
        self.portlist = []
        self.get_availables()

        self.port = port
        self.baudrate = baudrate

        self.arduinoexists = self.set_port(self.port)
        # self.py_serial = serial.Serial(
        #     port = port,
        #     baudrate = baudrate
        # )
        self.serial = None
        if self.arduinoexists:
            self.connect_port()
        self.pastValue = pastValue
        self.stat = stat

    def get_availables(self):
        list = sp.comports()
        self.portlist = []
        for i in list:
            self.portlist.append(i.device)
        return self.portlist
    
    def set_port(self, data):
        if data in self.get_availables():
            self.port = data
            self.arduinoexists = True
        else:
            self.arduinoexists = False
        return self.arduinoexists
        
    def connect_port(self):
        self.serial =  serial.Serial(self.port,self.baudrate)
        return
    
    def do_something(self, data):
        if data is not None:
            print("mesh data")
        















        

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
    
    def calculateNext(self, past, dest):
        next = [0,0,0,0,0,0]
        for i in range(len(dest)):
            if dest[i] > past[i]:
                next[i] = past[i] + 1
            elif dest[i] < past[i]:
                next[i] = past[i] - 1
            else:
                next[i] = past[i]
        return next
    
    def toStr(self,data):
        result = ""
        for element in data:
            result += str(int(element))
            result += " "
        return result
    
    def setMotor(self, past, dest):
        if self.stat == "tracking":
            next = self.calculateNext(past, dest)
        else:
            next = dest
        self.toStr(next)
        print(self.toStr(next).encode())
        self.py_serial.write(self.toStr(next).encode())
        return next
        # ret = self.arrToString(command.tolist())
        # self.pastValue = ret
        # print("motor ret " , ret)
        # self.py_serial.write(ret.encode())
        
    