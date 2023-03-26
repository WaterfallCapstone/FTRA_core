import numpy as np

class DataController:
    def __init__(self,env):
        self.env = env
        self.arm_length = np.array([0,0,0,0,0])
        self.camera_offset = np.array([0,0])
        self.motor_offset_angle = np.pi
        self.motor_value = np.array([0,0,0,0,0])
        self.destination_distance = 0

        self.get_config()
        return
    
    def str_to_fraction(self,data):
        splitdata = data.split('/')
        return float(splitdata[0]) / float(splitdata[1])
    
    # todo
    #########################################################
    def fraction_to_str(self,data):
        return
    
    #########################################################
        
    def get_config(self):
        config = self.env.config

        self.arm_length[0] = float(config['arm_length']['base_height'])
        self.arm_length[1] = float(config['arm_length']['arm_1'])
        self.arm_length[2] = float(config['arm_length']['arm_2'])
        self.arm_length[3] = float(config['arm_length']['arm_hor'])
        self.arm_length[4] = float(config['arm_length']['arm_ver'])

        self.camera_offset = np.array([float(config['cam_offset']['hor']),float(config['cam_offset']['ver'])])

        self.motor_offset_angle = np.pi * self.str_to_fraction(config['motor']['angle_offset'])

        self.motor_value[0] = np.pi * self.str_to_fraction(config['motor']['default_0'])
        self.motor_value[1] = np.pi * self.str_to_fraction(config['motor']['default_1'])
        self.motor_value[2] = np.pi * self.str_to_fraction(config['motor']['default_2']) - self.motor_offset_angle
        self.motor_value[3] = np.pi * self.str_to_fraction(config['motor']['default_3'])
        self.motor_value[4] = np.pi * self.str_to_fraction(config['motor']['default_4'])
        
        self.destination_distance = float(config['destination']['distance'])
    
    
    def print_env(self):
        print("default arm_length           : ",self.arm_length)
        print("default camera_offset        : ",self.camera_offset)
        print("default motor_offset_angle   : ",self.motor_offset_angle)
        print("default motor_value          : ",self.motor_value)
        print("default destination_distance : ",self.destination_distance)
