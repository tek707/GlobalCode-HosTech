from flask import Flask, render_template, request,redirect
from gpiozero import LED, MotionSensor
import RPi.GPIO as GPIO
import time
app = Flask(__name__)
ledgreen = LED(17)
yellowled = LED(26)
pir = MotionSensor(20)

ledgreen.off()
#sTART OF ULTRASONICE SENSOR CODE

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24


yellowled.off()
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
    

#END OF ULTRASONNIC SENSOR CODE



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def aboutus():
    return render_template('about.html')


@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/homepage.html')
def homepage():
    return render_template('homepage.html')



@app.post('/door/on')
def door_open():
     while True:
 
        dist = distance()
        if dist > 200:
                
            ledgreen.on()
              
        else:
                
            ledgreen.off()
                
           
       
            
        time.sleep(1)
            
        return redirect("/services.html")

@app.post('/door/off')
def door_offline():
    ledgreen.on()
    return redirect("/services.html")

@app.post('/motionsensor/on')
def motionsensor_on():
    pir.wait_for_motion()
    yellowled.on()
    return redirect("/services.html")

@app.post('/motionsensor/off')
def motionsensor_off():
    pir.wait_for_no_motion()
    yellowled.off()
    return redirect("/services.html")


@app.post('/light/on')
def light_on():
   
    yellowled.on()
    return redirect("/services.html")


@app.post('/light/off')
def light_off():
   
    yellowled.off()
    return redirect("/services.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
