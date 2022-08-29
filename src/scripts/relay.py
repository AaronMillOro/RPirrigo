"""
Script to test a the activation of a 12V relay 
through the RPI 3b+ pins 36 and 16
The activated relay will trigger the peristaltic pumping mechanism
"""
from time import sleep
import RPi.GPIO as GPIO


relay_pin = 36
relay_pin2 = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(relay_pin2, GPIO.OUT, initial=GPIO.LOW)

try:
    sleep(5)
    #GPIO.output(relay_pin, GPIO.HIGH)
    #GPIO.output(relay_pin2, GPIO.LOW)
    #print("pin", relay_pin2)
    #sleep(25)
    #GPIO.output(relay_pin, GPIO.LOW)
    GPIO.output(relay_pin2, GPIO.HIGH)
    print("pin 2", relay_pin2)
    sleep(35)
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()
