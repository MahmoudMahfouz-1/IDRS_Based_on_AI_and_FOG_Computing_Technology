import RPi.GPIO as GPIO

# Pin configuration for the motor drivers
MOTOR1_FRONT_PIN = 4
MOTOR1_BACK_PIN = 17
MOTOR2_FRONT_PIN = 27
MOTOR2_BACK_PIN = 22
MOTOR3_FRONT_PIN = 5
MOTOR3_BACK_PIN = 6
MOTOR4_FRONT_PIN = 13
MOTOR4_BACK_PIN = 19

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR1_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR1_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR2_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR2_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR3_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR3_BACK_PIN, GPIO.OUT)
GPIO.setup(MOTOR4_FRONT_PIN, GPIO.OUT)
GPIO.setup(MOTOR4_BACK_PIN, GPIO.OUT)

# Set up PWM for the motor drivers
MOTOR1_FRONT_PWM = GPIO.PWM(MOTOR1_FRONT_PIN, 100)
MOTOR1_BACK_PWM = GPIO.PWM(MOTOR1_BACK_PIN, 100)
MOTOR2_FRONT_PWM = GPIO.PWM(MOTOR2_FRONT_PIN, 100)
MOTOR2_BACK_PWM = GPIO.PWM(MOTOR2_BACK_PIN, 100)
MOTOR3_FRONT_PWM = GPIO.PWM(MOTOR3_FRONT_PIN, 100)
MOTOR3_BACK_PWM = GPIO.PWM(MOTOR3_BACK_PIN, 100)
MOTOR4_FRONT_PWM = GPIO.PWM(MOTOR4_FRONT_PIN, 100)
MOTOR4_BACK_PWM = GPIO.PWM(MOTOR4_BACK_PIN, 100)

# Start PWM for the motor drivers
MOTOR1_FRONT_PWM.start(0)
MOTOR1_BACK_PWM.start(0)
MOTOR2_FRONT_PWM.start(0)
MOTOR2_BACK_PWM.start(0)
MOTOR3_FRONT_PWM.start(0)
MOTOR3_BACK_PWM.start(0)
MOTOR4_FRONT_PWM.start(0)
MOTOR4_BACK_PWM.start(0)

# Define the functions to control the car
def forward(speed):
    MOTOR1_FRONT_PWM.ChangeDutyCycle(speed)
    MOTOR1_BACK_PWM.ChangeDutyCycle(0)
#     MOTOR2_FRONT_PWM.ChangeDutyCycle(speed)
#     MOTOR2_BACK_PWM.ChangeDutyCycle(0)
#     MOTOR3_FRONT_PWM.ChangeDutyCycle(speed)
#     MOTOR3_BACK_PWM.ChangeDutyCycle(0)
#     MOTOR4_FRONT_PWM.ChangeDutyCycle(speed)
#     MOTOR4_BACK_PWM.ChangeDutyCycle(0)

def left(speed):
    MOTOR1_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR1_BACK_PWM.ChangeDutyCycle(speed)
    MOTOR2_FRONT_PWM.ChangeDutyCycle(speed)
    MOTOR2_BACK_PWM.ChangeDutyCycle(0)
    MOTOR3_FRONT_PWM.ChangeDutyCycle(speed)
    MOTOR3_BACK_PWM.ChangeDutyCycle(0)
    MOTOR4_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR4_BACK_PWM.ChangeDutyCycle(speed)

def right(speed):
    MOTOR1_FRONT_PWM.ChangeDutyCycle(speed)
    MOTOR1_BACK_PWM.ChangeDutyCycle(0)
    MOTOR2_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR2_BACK_PWM.ChangeDutyCycle(speed)
    MOTOR3_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR3_BACK_PWM.ChangeDutyCycle(speed)
    MOTOR4_FRONT_PWM.ChangeDutyCycle(speed)
    MOTOR4_BACK_PWM.ChangeDutyCycle(0)

def stop():
    MOTOR1_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR1_BACK_PWM.ChangeDutyCycle(0)
    MOTOR2_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR2_BACK_PWM.ChangeDutyCycle(0)
    MOTOR3_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR3_BACK_PWM.ChangeDutyCycle(0)
    MOTOR4_FRONT_PWM.ChangeDutyCycle(0)
    MOTOR4_BACK_PWM.ChangeDutyCycle(0)
