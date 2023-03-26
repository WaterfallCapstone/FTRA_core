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
    