import numpy as np

class MotorLocation:
    def __init__(self,data):
        self.data = data
        
        return
    
    def cal_armtip_loc_polar(self):
        motor_value = self.data.get_motor_value()
        arm_length = self.data.get_arm_length()
        motor_offset_angle = self.data.get_motor_offset_angle()
        armtip_loc_polar = np.array([1.0 ,0.0, 0.0])

        angle_ab = (3/2) * np.pi - motor_value[2] - motor_offset_angle
        # length2 = arm_length[2]+arm_length[3]
        length2 = arm_length[2]
        c_square = np.power(arm_length[1],2) + np.power(length2,2) - 2*arm_length[1]*arm_length[2]*np.cos(angle_ab)
        armtip_loc_polar[0] = np.sqrt(c_square)        
        armtip_loc_polar[2] = motor_value[0]
        
        cos_ac = (np.power(arm_length[1],2) - np.power(length2,2) + c_square) / (2*arm_length[1]*armtip_loc_polar[0])            
        if cos_ac >= -1 and cos_ac <= 1:
            armtip_loc_polar[1] = np.arccos(cos_ac) + motor_value[1] - np.pi/2
        # print(armtip_loc_polar)
        return armtip_loc_polar
    
    def cal_armtip_dir_polar(self):
        motor_value = self.data.get_motor_value()
        # motor_offset_angle = self.data.get_motor_offset_angle()
        return np.array([1,np.pi/2,motor_value[0]])

    
    def armtip_loc_polar_to_cart(self):
        armtip_loc_polar = self.data.get_armtip_loc_polar()
        
        armlength = self.data.get_motor_value()
        armtip_loc_cart = np.array([0,0,0])

        r = armtip_loc_polar[0]
        theta = armtip_loc_polar[1]
        phi = armtip_loc_polar[2]
        armtip_loc_cart[0] = r * np.sin(theta) * np.cos(phi)
        armtip_loc_cart[1] = r * np.sin(theta) * np.sin(phi)
        armtip_loc_cart[2] = r * np.cos(theta)
        
        armtip_loc_cart[2] += armlength[0]

        return armtip_loc_cart