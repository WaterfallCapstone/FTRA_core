import platform
import configparser
from time import strftime
import os
from pathlib import Path
import sys

class env:
    def __init__(self):
        if(sys.argv[0] == "__main__.py"):
            self.EnvPath = os.path.abspath(os.path.join(os.getcwd(),r'Data',r'Config.txt'))
        else:
            self.EnvPath = os.path.abspath(os.path.join(os.getcwd(),sys.argv[0],r'Data',r'Config.txt'))
        
        print(self.EnvPath)
        self.config = configparser.ConfigParser()
        self.config_read()

    def get_config(self,data1,data2):
        return self.config[data1][data2]


    def config_read(self):
        
        # 설정파일 읽기
        self.config.read(self.EnvPath, encoding='utf-8') 

        # 설정파일의 색션 확인
        # self.config.sections()
        # print(self.config)

        self.version_read()
    
    def version_read(self):

        ver = self.config['system']['version']
        title = self.config['system']['title']
        print(title,ver)

    # todo : set config 
    ################################################################################
    def set_config(self,param1, param2, data):
        return
    ##################################################################################

    def save_config(self):
        with open(self.EnvPath, 'w+', encoding='utf-8') as configfile:
            self.config.write(configfile)
        return
    

    def config_generator(self):
        config = configparser.ConfigParser()

        config['system'] = {}
        config['system']['title'] = 'FTRA_CORE'
        config['system']['version'] = '1.0.0'
        config['system']['update'] = strftime('%Y-%m-%d %H:%M:%S')

        config['arm_length'] = {}
        config['arm_length']['base_height'] = '15'
        config['arm_length']['arm_1'] = '20'
        config['arm_length']['arm_2'] = '20'
        config['arm_length']['arm_hor'] = '5'
        config['arm_length']['arm_ver'] = '2'

        config['cam_offset'] = {}
        config['cam_offset']['hor'] = '0'
        config['cam_offset']['ver'] = '0'

        config['motor'] = {}
        config['motor']['angle_offset'] = '1/3' # value * pi | value form : fraction split by /
        config['motor']['default_0'] = '1/2'
        config['motor']['default_1'] = '1/2'
        config['motor']['default_2'] = '1/2' # value * pi - angle_offset
        config['motor']['default_3'] = '1/1'
        config['motor']['default_4'] = '1/2'

        config['destination'] = {} 
        config['destination']['distance'] = '0.5'

        with open(self.EnvPath, 'w+', encoding='utf-8') as configfile:
            config.write(configfile)