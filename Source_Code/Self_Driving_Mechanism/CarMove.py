
import RPi.GPIO as GPIO
import time

# Pin configuration for the motor drivers
# motor1 front right
# EN, Front, Back
# 3,     5,   7
#
# motor2 front left
# EN, Front, Back
# 11,     13,   15
#
#
# motor3 back right
# EN, Front, Back
# 19,     21,   23
#
#
# motor4 back left
# EN, Front, Back
# 29,     31,   33

#MOTOR FRONT RIGHT
MOTOR1_ENABLE_PIN = 3
MOTOR1_FRONT_PIN = 5
MOTOR1_BACK_PIN = 7
#MOTOR FRONT LEFT
MOTOR2_ENABLE_PIN = 11
MOTOR2_FRONT_PIN = 13
MOTOR2_BACK_PIN = 15
#MOTOR BACK RIGHT
MOTOR3_ENABLE_PIN = 19
MOTOR3_FRONT_PIN = 21
MOTOR3_BACK_PIN = 23
#MOTOR BACK LEFT
MOTOR4_ENABLE_PIN = 29
MOTOR4_FRONT_PIN = 31
MOTOR4_BACK_PIN = 33

# Set up the GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR1_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR1_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR1_ENABLE_PIN, GPIO.OUT)
GPIO.setup(MOTOR2_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR2_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR2_ENABLE_PIN, GPIO.OUT)
GPIO.setup(MOTOR3_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR3_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR3_ENABLE_PIN, GPIO.OUT)
GPIO.setup(MOTOR4_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR4_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR4_ENABLE_PIN, GPIO.OUT)

# Set up PWM for the motor drivers
MOTOR1_PWM = GPIO.PWM(MOTOR1_ENABLE_PIN, 100)
MOTOR2_PWM = GPIO.PWM(MOTOR2_ENABLE_PIN, 100)
MOTOR3_PWM = GPIO.PWM(MOTOR3_ENABLE_PIN, 100)
MOTOR4_PWM = GPIO.PWM(MOTOR4_ENABLE_PIN, 100)

# Start PWM for the motor drivers
MOTOR1_PWM.start(0)
MOTOR2_PWM.start(0)
MOTOR3_PWM.start(0)
MOTOR4_PWM.start(0)

# Define the functions to control the car
def move(speedR, speedL):
    MOTOR1_PWM.ChangeDutyCycle(abs(speedR))
    MOTOR2_PWM.ChangeDutyCycle(abs(speedL))
    MOTOR3_PWM.ChangeDutyCycle(abs(speedR))
    MOTOR4_PWM.ChangeDutyCycle(abs(speedL))
    if speedR < 0 and speedL < 0 : # Backward
        backward()
    elif speedR < 0 and speedL > 0 : # Right
        turnRight()
    elif speedR > 0 and speedL < 0 : # Left
        turnLeft()
    elif speedR > 0 and speedL > 0 : # Forward
        forward()
    elif speedR == 0 and speedL == 0 :
        stop()



def forward():
    GPIO.output(MOTOR1_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR1_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR2_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR2_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR3_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR3_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR4_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR4_BACK_PIN, GPIO.LOW)

def turnLeft():
    GPIO.output(MOTOR1_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR1_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR2_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR2_BACK_PIN, GPIO.HIGH)

    GPIO.output(MOTOR3_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR3_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR4_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR4_BACK_PIN, GPIO.HIGH)

def turnRight():
    GPIO.output(MOTOR1_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR1_BACK_PIN, GPIO.HIGH)

    GPIO.output(MOTOR2_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR2_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR3_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR3_BACK_PIN, GPIO.HIGH)

    GPIO.output(MOTOR4_FRONT_PIN, GPIO.HIGH)
    GPIO.output(MOTOR4_BACK_PIN, GPIO.LOW)

def backward():
    GPIO.output(MOTOR1_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR1_BACK_PIN, GPIO.HIGH)

    GPIO.output(MOTOR2_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR2_BACK_PIN, GPIO.HIGH)

    GPIO.output(MOTOR3_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR3_BACK_PIN, GPIO.HIGH)

    GPIO.output(MOTOR4_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR4_BACK_PIN, GPIO.HIGH)


def stop():
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
    MOTOR3_PWM.ChangeDutyCycle(0)
    MOTOR4_PWM.ChangeDutyCycle(0)
    GPIO.output(MOTOR1_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR1_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR2_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR2_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR3_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR3_BACK_PIN, GPIO.LOW)

    GPIO.output(MOTOR4_FRONT_PIN, GPIO.LOW)
    GPIO.output(MOTOR4_BACK_PIN, GPIO.LOW)

