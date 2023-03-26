import Settings
from Modules import Camera
from Modules import Motor
from Modules import DataController

env = Settings.env()
Data = DataController(env)
CamLocation = Camera.CamLocation(env)
MotorController = Motor.MotorController(env)


Data.print_env()