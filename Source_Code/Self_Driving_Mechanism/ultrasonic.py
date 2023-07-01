import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Front sensor
GPIO_TRIGGER_F = 35
GPIO_ECHO_F = 37

# left sensor
GPIO_TRIGGER_L = 16
GPIO_ECHO_L = 18

# Right sensor
GPIO_TRIGGER_R = 22
GPIO_ECHO_R = 24

GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER_F, GPIO.OUT)
GPIO.setup(GPIO_ECHO_F, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)
GPIO.output(GPIO_TRIGGER_F, False)
GPIO.output(GPIO_TRIGGER_L, False)
GPIO.output(GPIO_TRIGGER_R, False)
time.sleep(1)

class UltraSonic():

    def __init__ (self):
        print("UltraSonic Started")

    def DistanceF(self):
        #trigger the ultrasonic sensor for a very short period (10us).
        GPIO.output(GPIO_TRIGGER_F, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_F, False)

        while GPIO.input(GPIO_ECHO_F) == 0:
            pass
        StartTime = time.time() #start timer once the pulse is sent completely and echo becomes high or 1
        while GPIO.input(GPIO_ECHO_F) == 1:
            pass
        StopTime = time.time() #stop the timer once the signal is completely received  and echo again becomes 0

        TimeElapsed = StopTime - StartTime # This records the time duration for which echo pin was high
        speed=34300 #speed of sound in air 343 m/s  or 34300cm/s
        twicedistance = (TimeElapsed * speed) #as time elapsed accounts for amount of time it takes for the pulse to go and come back
        distance=twicedistance/2  # to get actual distance simply divide it by 2
        time.sleep(.01)
        #print("dis_f In UltraSonic =", distance)
        return round(distance,2) # round off upto 2 decimal points

    def DistanceL(self):

        #trigger the ultrasonic sensor for a very short period (10us).
        GPIO.output(GPIO_TRIGGER_L, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_L, False)

        while GPIO.input(GPIO_ECHO_L) == 0:
            pass
        StartTime = time.time() #start timer once the pulse is sent completely and echo becomes high or 1
        while GPIO.input(GPIO_ECHO_L) == 1:
            pass
        StopTime = time.time() #stop the timer once the signal is completely received  and echo again becomes 0

        TimeElapsed = StopTime - StartTime # This records the time duration for which echo pin was high
        speed=34300 #speed of sound in air 343 m/s  or 34300cm/s
        twicedistance = (TimeElapsed * speed) #as time elapsed accounts for amount of time it takes for the pulse to go and come back
        distance=twicedistance/2  # to get actual distance simply divide it by 2
        time.sleep(.01)
        #print("dis_L In UltraSonic =", distance)
        return round(distance,2) # round off upto 2 decimal points
    def DistanceR(self):
        GPIO.output(GPIO_TRIGGER_R, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_R, False)
        while GPIO.input(GPIO_ECHO_R) == 0:
            pass
        StartTime = time.time()
        while GPIO.input(GPIO_ECHO_R) == 1:
            pass
        StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        speed=34300
        twicedistance = (TimeElapsed * speed)
        distance=twicedistance/2
        time.sleep(.01)
        return round(distance,2)
