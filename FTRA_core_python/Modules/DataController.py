import numpy as np

class DataController:
    def __init__(self,env):
        self.env = env
        self.arm_length = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        self.camera_offset = np.array([0.0,0.0])
        self.motor_offset_angle = np.pi
        self.motor_value = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
        self.motor_dest = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
        self.destination_distance = 0.0
        self.tickrate = 100
        self.axis = 4
        self.isface = False
        self.image = ""

        self.armtip_loc_polar = np.array([self.arm_length[1] + self.arm_length[2] ,np.pi/2, np.pi/2])
        self.armtip_loc_cart = np.array([0.0,0.0,0.0])
        self.armtip_dir_polar = np.array([1.0,0.0,0.0])

        # self.cam_loc_polar = np.array([self.arm_length[1] + self.arm_length[2] ,np.pi/2, np.pi/2])
        self.cam_loc_cart = np.array([0.0,0.0,0.0])
        self.cam_dir_polar = np.array([1.0,0.0,0.0])

        self.camface_loc_polar = np.array([70.0, 0.0, np.pi / 2])
        self.camface_dir_cart = np.array([0.0, 0.0, 0.0])

        self.face_loc_cart = np.array([0.0, 0.0, 0.0])
        self.face_lookat = np.array([0.0, 0.0, 0.0])


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
        print(float(config['arm_length']['arm_1']))

        self.arm_length[0] = float(config['arm_length']['base_height'])
        self.arm_length[1] = float(config['arm_length']['arm_1'])
        self.arm_length[2] = float(config['arm_length']['arm_2'])
        self.arm_length[3] = float(config['arm_length']['arm_3'])
        self.arm_length[4] = float(config['arm_length']['arm_4'])
        self.arm_length[5] = float(config['arm_length']['arm_5'])
        self.arm_length[6] = float(config['arm_length']['arm_6'])

        self.camera_offset = np.array([float(config['cam_offset']['hor']),float(config['cam_offset']['ver'])])

        self.motor_offset_angle = np.pi * self.str_to_fraction(config['motor']['angle_offset'])

        self.motor_value[0] = np.pi * self.str_to_fraction(config['motor']['default_0'])
        self.motor_value[1] = np.pi * self.str_to_fraction(config['motor']['default_1'])
        self.motor_value[2] = np.pi * self.str_to_fraction(config['motor']['default_2']) - self.motor_offset_angle
        self.motor_value[3] = np.pi * self.str_to_fraction(config['motor']['default_3'])
        self.motor_value[4] = np.pi * self.str_to_fraction(config['motor']['default_4'])
        self.motor_value[5] = np.pi * self.str_to_fraction(config['motor']['default_5'])
        
        self.destination_distance = float(config['destination']['distance'])

        self.tickrate = int(config['system']['tickrate'])
        self.axis = int(config['system']['axis'])
    #############################################################
    def set_isface(self,data):
        self.isface = data

    def set_armtip_loc_polar(self,data):
        self.armtip_loc_polar = data
    
    def set_armtip_loc_cart(self,data):
        self.armtip_loc_cart = data

    def set_armtip_dir_polar(self,data):
        self.armtip_dir_polar = data
    
    # def set_cam_loc_polar(self,data):
    #     self.cam_loc_polar = data
    
    def set_cam_loc_cart(self,data):
        self.cam_loc_cart = data

    def set_cam_dir_polar(self,data):
        self.cam_dir_polar = data
    
    def set_face_loc_cart(self,data):
        self.face_loc_cart = data
    
    def set_face_lookat(self,data):
        self.face_lookat = data

    def set_camface_loc_polar(self,data):
        self.camface_loc_polar = data
    
    def set_camface_dir_cart(self,data):
        self.camface_dir_cart = data
    
    def set_image(self,data):
        self.image = data

    def set_motor_value(self,data):
        self.motor_value = data
        
    def set_motor_dest(self,data):
        self.motor_dest = data


    ###########################################################
    def get_isface(self):
        return self.isface
    
    def get_motor_value(self, isnumpy = True, israd = True):
        if israd:
            if isnumpy:
                return self.motor_value
            else:
                motor_data = []
                for i in self.motor_value:
                    motor_data.append(i)
                return motor_data
        else:
            if isnumpy:
                value = self.motor_value
                # print(value)
                for i in range(value.size) :
                    value[i] = np.rad2deg(value[i])
                return value
            else:
                motor_data = []
                for i in self.motor_value:
                    motor_data.append(np.rad2deg(i))
                return motor_data
    
    def get_arm_length(self):
        return self.arm_length
    
    def get_motor_offset_angle(self):
        return self.motor_offset_angle
    
    def get_cam_offset(self):
        return self.camera_offset
    
    def get_armtip_loc_polar(self, isnumpy = True):
        if(isnumpy):
            return self.armtip_loc_polar
        else:
            data = [self.armtip_loc_polar[0], np.rad2deg(self.armtip_loc_polar[1]), np.rad2deg(self.armtip_loc_polar[2])]
            data = list([float(x) for x in data])
            return data
        
    def get_armtip_loc_cart(self, isnumpy = True):
        if(isnumpy):
            return self.armtip_loc_cart
        else:
            data = [self.armtip_loc_cart[0], self.armtip_loc_cart[1], self.armtip_loc_cart[2]]
            data = list([float(x) for x in data])
            return data
        
    def get_armtip_dir_polar(self, isnumpy = True):
        if(isnumpy):
            return self.armtip_dir_polar
        else:
            data = [self.armtip_dir_polar[0], np.rad2deg(self.armtip_dir_polar[1]), np.rad2deg(self.armtip_dir_polar[2])]
            data = list([float(x) for x in data])
            return data
        
    
    def get_camface_loc_polar(self):
        return self.camface_loc_polar
    
    def get_camface_dir_cart(self):
        return self.camface_dir_cart
    
    def get_cam_loc_cart(self,isnumpy = True):
        if(isnumpy):
            return self.cam_loc_cart
        else:
            data = [self.cam_loc_cart[0], self.cam_loc_cart[1], self.cam_loc_cart[2]]
            data = list([float(x) for x in data])
            return data
    
    def get_face_loc_cart(self):
        return self.face_loc_cart
    
    def get_cam_dir_polar(self,isnumpy = True):
        if(isnumpy):
            return self.cam_dir_polar
        else:
            data = [self.cam_dir_polar[0], np.rad2deg(self.cam_dir_polar[1]), np.rad2deg(self.cam_dir_polar[2])]
            data = list([float(x) for x in data])
            return data
    
    def get_image(self):
        return self.image

    def get_destination_distance(self):
        return self.destination_distance

    def get_motor_dest(self, israd = True):
        if israd:
            return self.motor_dest
        else:
            motor_dest = []
            for i in self.motor_dest:
                motor_dest.append(np.rad2deg(i))
            return np.array(motor_dest)
            
    
    def print_env(self):
        print("default arm_length           : ",self.arm_length)
        print("default camera_offset        : ",self.camera_offset)
        print("default motor_offset_angle   : ",self.motor_offset_angle)
        print("default motor_value          : ",self.motor_value)
        print("default destination_distance : ",self.destination_distance)
        print("default tickrate             : ",self.tickrate)
        print("default axis                 : ",self.axis)