import numpy as np

class CamLocation:
    def __init__(self, env):
        self.env = env
    
    def printenv(self):
        print(self.env.hello)

    def changeenv(self,data):
        self.env.sethello(data)

    def printhello(self):
        print(self.env.gethello())