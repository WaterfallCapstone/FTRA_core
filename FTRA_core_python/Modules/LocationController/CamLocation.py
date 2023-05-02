import numpy as np

class CamLocation4:
    def __init__(self, data):
        self.data = data
        self.cam_offset_cart = self.cal_cam_offset_cart()
        self.cam_rot = np.array([0.0,0.0,0.0,0.0])
        self.cam_trans = np.array([0.0,0.0,0.0,0.0])

    def cal_cam_offset_cart(self):
        cam_offset = self.data.get_cam_offset()
        return np.array([cam_offset[0],0.0,cam_offset[1],0.0])
    
    def cal_cam_loc_cart(self):
        armtip_loc_cart = self.data.get_armtip_loc_cart()
        armtip_loc_cart = np.append(armtip_loc_cart,0.0)
        armtip_dir_polar = self.data.get_armtip_dir_polar()

        roll = armtip_dir_polar[1]
        pitch = np.pi/2 - armtip_dir_polar[2]
        roll_matrix = np.array(
            [
                [np.cos(roll), -np.sin(roll), 0, 0],
                [np.sin(roll), np.cos(roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        pitch_matrix = np.array(
            [
                [1,0,0,0],
                [0,np.cos(pitch),-np.sin(pitch),0],
                [0,np.sin(pitch),np.cos(pitch),0],
                [0,0,0,1]
            ]
        )
        self.cam_rot = roll_matrix @ (pitch_matrix @ self.cam_offset_cart)
        self.cam_trans = self.cam_rot + armtip_loc_cart


        return self.cam_trans[:3]
    
    def cal_cam_dir_polar(self):
        motor_value = self.data.get_motor_value()
        armtip_dir_polar = self.data.get_armtip_dir_polar()
        return np.array([1, armtip_dir_polar[1], armtip_dir_polar[2] + motor_value[4] - np.pi / 2])


class CamLocation5:
    def __init__(self, data):
        self.data = data
    

    def default_cam_offset_cart(self):
        arm_length = self.data.get_arm_length()
        return np.array([arm_length[3],0,arm_length[4]])


class CamLocation6:
    def __init__(self, data):
        self.data = data
        self.cam_offset_cart = self.cal_cam_offset_cart()
        self.cam_rot = np.array([0.0,0.0,0.0,0.0])
        self.cam_trans = np.array([0.0,0.0,0.0,0.0])

    def cal_cam_offset_cart(self):
        armlength = self.data.get_arm_length()
        motorvalue = self.data.get_motor_value()
        base = np.array([0.0,0.0,armlength[6],0.0])
        yaw = np.pi - motorvalue[5]
        yaw_matrix = np.array(
            [
                [np.cos(yaw), 0 , np.sin(yaw), 0],
                [0, 1, 0, 0],
                [-np.sin(yaw),0,np.cos(yaw),0],
                [0,0,0,1]
            ]
        )
        base_next = yaw_matrix @ base
        
        base_next[0] += armlength[5]
        
        roll = motorvalue[4] - np.pi/2
        roll_matrix = np.array(
            [
                [np.cos(roll), -np.sin(roll), 0, 0],
                [np.sin(roll), np.cos(roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        
        after_roll = roll_matrix @ base_next
        
        after_roll[2] += armlength[4]
        after_roll[0] += armlength[3]

        return after_roll
        
        
    
    def cal_cam_loc_cart(self):
        armtip_loc_cart = self.data.get_armtip_loc_cart()
        armtip_loc_cart = np.append(armtip_loc_cart,0.0)
        armtip_dir_polar = self.data.get_armtip_dir_polar()
        # print(armtip_dir_polar)
        roll = armtip_dir_polar[2]
        pitch = np.pi/2 - armtip_dir_polar[1]
        roll_matrix = np.array(
            [
                [np.cos(roll), -np.sin(roll), 0, 0],
                [np.sin(roll), np.cos(roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        pitch_matrix = np.array(
            [
                [1,0,0,0],
                [0,np.cos(pitch),-np.sin(pitch),0],
                [0,np.sin(pitch),np.cos(pitch),0],
                [0,0,0,1]
            ]
        )
        base = self.cal_cam_offset_cart()
        self.cam_rot = roll_matrix @ (pitch_matrix @ base)
        self.cam_trans = self.cam_rot + armtip_loc_cart
        # print(self.cam_trans)
        return self.cam_trans[:3]
    
    def cal_cam_dir_polar(self):
        motorvalue = self.data.get_motor_value()
        base = np.array([0.0,0.0,1,0.0])
        yaw = np.pi - motorvalue[5]
        armtip_dir_polar = self.data.get_armtip_dir_polar()
        
        yaw_matrix = np.array(
            [
                [np.cos(yaw), 0 , np.sin(yaw), 0],
                [0, 1, 0, 0],
                [-np.sin(yaw),0,np.cos(yaw),0],
                [0,0,0,1]
            ]
        )
        roll = motorvalue[4] - np.pi/2
        roll_matrix = np.array(
            [
                [np.cos(roll), -np.sin(roll), 0, 0],
                [np.sin(roll), np.cos(roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        armtip_roll = armtip_dir_polar[2]
        armtip_roll_matrix = np.array(
            [
                [np.cos(armtip_roll), -np.sin(armtip_roll), 0, 0],
                [np.sin(armtip_roll), np.cos(armtip_roll), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ]
        )
        
        after_roll = armtip_roll_matrix @ (roll_matrix @ (yaw_matrix @ base))
        result = np.array([1,0.0,0.0])       
        if after_roll[2] >= -1 and after_roll[2] <= 1:
            result[1] = np.arccos(after_roll[2])
        result[2] = np.arctan(after_roll[1]/after_roll[0])
        return result
