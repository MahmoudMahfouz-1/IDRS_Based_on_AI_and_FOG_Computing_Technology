import numpy as np
import cv2
import CarMove
from ultrasonic import UltraSonic
from time import sleep
speed = 100
US=UltraSonic()
class LaneDetection(object):
    def __init__(self):
        #self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.red = False
        self.num_left_lines = 0
        self.num_right_lines = 0
        self.lane_detection()

    def lane_detection(self):
        try:
            while True:
                _, image = self.cap.read()
                lane_image = np.copy(image)
                lane_image, self.red = self.check_for_red(lane_image)

                if self.red:
                    print('Red detected')
                else:
                    canny = self.canny(lane_image)
                    roi = self.region_of_interest(canny)
                    lane = cv2.bitwise_and(canny, roi)
                    lines = cv2.HoughLinesP(lane, 1, np.pi/180, 30, np.array([]), minLineLength=20, maxLineGap=5)
                    self.average_slope_intercept(lines, lane_image)
                    line_image = self.display_lines(lines, lane_image)
                    lane_image = cv2.addWeighted(lane_image, 1, line_image, 1, 0)

#                     cv2.imshow('canny', canny)
#                     cv2.imshow('roi', roi)
#                     cv2.imshow('lane', lane)
#                     cv2.imshow('line', line_image)
                    cv2.imshow('frame', lane_image)  # display image
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
    

                
                        ######### Self Driving code ##########
                    left = self.num_left_lines
                    right = self.num_right_lines
                    red = self.red
                    dis_f = US.DistanceF()
                                        #print("HEREE")
                    print("dis_f=", dis_f)
                    dis_L = US.DistanceL()
                    print("dis_f=", dis_f)
                    dis_R = US.DistanceR()
                                        # Get current distance from ultrasonic sensors

                    print("left=",left)
                    print("right=",right)
                    print("dis_f=", dis_f)
                    print("dis_L=", dis_L)
                    print("dis_R=", dis_R)
                    CarMove.move(20,20)
                    if red : # Stop the car if condition is true
                        CarMove.move(0,0)
                    elif dis_f < 15 :
                        CarMove.move(0,0)
                    elif(left>right): # if left is more ==> move left by stopping the left wheel.
                        CarMove.move(speed,-1 * speed)

                    elif(right>left): # if right is more==> move right by stopping the right wheel.
                        CarMove.move(-1 * speed,speed)

                    """
                    if dis_f < 30 and dis_R > 20 and dis_L < 15:

                        CarMove.move(-1 * speed, speed)

                    elif dis_f < 30 and dis_L > 20 and dis_R < 15:
                        CarMove.move(speed, -1 * speed)
                    """

        finally:
            self.cap.release()
            cv2.destroyAllWindows()

    def check_for_red(self, image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Red HSV Range
        low_red = np.array([157, 56, 0])
        high_red = np.array([179, 255, 255])

        mask = cv2.inRange(hsv, low_red, high_red)
        blur = cv2.GaussianBlur(mask, (15, 15), 0)
        contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        status = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 20000:
                status = 1
                cv2.drawContours(image, contour, -1, (0, 0, 255), 3)
                cv2.putText(image, 'RED STOP', (240, 320), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
        return (image, status)

    def average_slope_intercept(self, lines, image):
        left_fit = []
        right_fit = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                intercept = parameters[1]
                if slope < 0:
                    right_fit.append((slope, intercept))
                else:
                    left_fit.append((slope, intercept))

        left_fitavg = np.average(left_fit, axis=0)
        right_fitavg = np.average(right_fit, axis=0)
        self.num_left_lines = len(left_fit)
        self.num_right_lines = len(right_fit)
#         print("Number of left lines:", self.num_left_lines)
#         print("Number of right lines:", self.num_right_lines)
    def canny(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        canny = cv2.Canny(blur, 50, 150)  # lowerThreshold=50 UpperThreshold=150
        return canny

    def region_of_interest(self, image):
        height = image.shape[0]
        width = image.shape[1]
        region = np.array([[(100, height), (width-100, height), (width-100, height-120), (100, height-120)]])
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, region, 255)
        return mask

    def display_lines(self, lines, image):
        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                if len(line) > 0:
                    x1, y1, x2, y2 = line.reshape(4)
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        return line_image


if __name__ == '__main__':
    lane_detection = LaneDetection()