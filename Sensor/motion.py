import RPi.GPIO as GPIO
import time
from gpiozero import LED
from gpiozero import MotionSensor

yellowled = LED(20)
pir = MotionSensor(26)
yellowled.off()

while True:
    pir.wait_for_motion()
    print ("Motion detected")
    yellowled.on()
    pir.wait_for_no_motion()
    yellowled.off()
    print("motion stopped")
