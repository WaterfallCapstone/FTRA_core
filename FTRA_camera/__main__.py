import numpy as np
from flask import Flask, url_for, render_template
from flask_socketio import SocketIO, emit
from Modules import Config


config = Config()


tickrate = config.get_config('camera',"TICKRATE")




