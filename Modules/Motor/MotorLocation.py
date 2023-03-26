import numpy as np

class MotorLocation:
    def __init__(self,data):
        self.data = data
        
        return
    
    def cal_armtip_loc_polar(self):
        motor_value = self.data.get_motor_value()
        arm_length = self.data.get_arm_length()
        motor_offset_angle = self.data.get_motor_offset_angle()
        armtip_loc_polar = np.array([1 ,0, 0])

        angle_ab = (3/2) * np.pi - motor_value[2] - motor_offset_angle
        # length2 = arm_length[2]+arm_length[3]
        length2 = arm_length[2]
        c_square = np.power(arm_length[1],2) + np.power(length2,2) - 2*arm_length[1]*arm_length[2]*np.cos(angle_ab)
        armtip_loc_polar[0] = np.sqrt(c_square)        
        armtip_loc_polar[1] = motor_value[0]
        
        cos_ac = (np.power(arm_length[1],2) - np.power(length2,2) + c_square) / (2*arm_length[1]*armtip_loc_polar[0])            
    
        armtip_loc_polar[2] = np.arccos(cos_ac) + motor_value[1] - np.pi/2
        return armtip_loc_polar
    
    def cal_armtip_dir_polar(self):
        motor_value = self.data.get_motor_value()
        motor_offset_angle = self.data.get_motor_offset_angle()
        return np.array([1,motor_value[0],motor_value[1]+motor_value[2]+motor_offset_angle - np.pi])

    
    def armtip_loc_polar_to_cart(self):
        armtip_loc_polar = self.data.get_armtip_loc_polar()
        armtip_loc_cart = np.array([0,0,0])

        r = armtip_loc_polar[0]
        phi = armtip_loc_polar[1]
        theta = armtip_loc_polar[2]
        armtip_loc_cart[0] = r * np.sin(theta) * np.cos(phi)
        armtip_loc_cart[1] = r * np.sin(theta) * np.sin(phi)
        armtip_loc_cart[2] = r * np.cos(theta)

        return armtip_loc_cart