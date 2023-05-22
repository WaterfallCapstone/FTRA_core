import platform
import configparser
from time import strftime
import os
from pathlib import Path
import sys

class Config:
    def __init__(self):
        if(sys.argv[0] == "__main__.py"):
            self.EnvPath = os.path.abspath(os.path.join(os.getcwd(),r'Data',r'Config.txt'))
        else:
            temp = sys.argv[0]
            if "." in temp:
                temp = temp.split("/")[0]
            self.EnvPath = os.path.abspath(os.path.join(os.getcwd(),temp,r'Data',r'Config.txt'))
        
        print(self.EnvPath)
        self.config = configparser.ConfigParser()
        self.config_read()

    def get_config(self,data1,data2, type = "str"):
        result = self.config[str(data1)][str(data2)]
        if (type == "int"):
            return int(result)
        elif (type == "float"):
            return float(result)
        elif (type == "fraction"):
            tmp = result.split("/")
            return float(tmp[0]) / float(tmp[1])
        else:
            return result


    def config_read(self):
        self.config.read(self.EnvPath, encoding='utf-8') 


    def set_config(self,param1, param2, data):
        self.config[param1][param2] = str(data)
        self.save_config()
        return


    def save_config(self):
        with open(self.EnvPath, 'w+', encoding='utf-8') as configfile:
            self.config.write(configfile)
        return
