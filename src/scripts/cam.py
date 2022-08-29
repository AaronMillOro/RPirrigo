"""
Script to take a picture with the connected PiCamera and store the image
on the directory named "img"
"""

from picamera import PiCamera
import time


filename = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
cam = PiCamera()
cam.start_preview()
time.sleep(7)
STORAGE_DIR = "/RPirrigo/img/" + filename + ".jpg"
cam.capture(STORAGE_DIR)
cam.stop_preview()
cam.close()
