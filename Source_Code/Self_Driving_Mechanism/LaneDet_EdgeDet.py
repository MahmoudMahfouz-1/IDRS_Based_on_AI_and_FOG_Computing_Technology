import numpy as np
import cv2
import CarMove
from ultrasonic import UltraSonic
from time import sleep

speed = 100
US = UltraSonic()

class LaneDetection(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.red = False
        self.num_left_lines = 0
        self.num_right_lines = 0
        self.left_fit = None
        self.right_fit = None
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
                    lane_image = self.color_thresholding(lane_image)
                    canny = self.canny(lane_image)
                    roi = self.region_of_interest(canny)
                    lines = cv2.HoughLinesP(roi, rho=1, theta=np.pi/180, threshold=30, minLineLength=20, maxLineGap=5)
                    self.average_slope_intercept(lines, lane_image)
                    line_image = self.draw_lines(lines, lane_image)
                    lane_image = cv2.addWeighted(lane_image, 1, line_image, 1, 0)

                    cv2.imshow('frame', lane_image)  # display image
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break

                    ######### Self Driving code ##########
                    left = self.num_left_lines
                    right = self.num_right_lines
                    red = self.red
                    # Get current distance from ultrasonic sensors
                    dis_f = US.DistanceF()
                    dis_L = US.DistanceL()
                    dis_R = US.DistanceR()
                    print("left=", left)
                    print("right=", right)
                    print("dis_f=", dis_f)
                    print("dis_L=", dis_L)
                    print("dis_R=", dis_R)
                    if red: # Stop the car if red is detected
                        CarMove.move(0, 0)
                    elif dis_f < 15: # Stop the car if an obstacle is detected
                        CarMove.move(0, 0)
                    else:
                        pid_output = self.pid_controller(left, right)
                        CarMove.move(speed + pid_output, speed - pid_output)

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
        status = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 20000:
                status = True
                cv2.drawContours(image, contour, -1, (0, 0, 255), 3)
                cv2.putText(image, 'RED STOP', (240, 320), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
        return (image, status)

    def color_thresholding(self, image):
        # Convert image to HLS color space
        hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        # Define white and yellow color ranges
        low_white = np.array([0, 200, 0])
        high_white = np.array([255, 255, 255])
        low_yellow = np.array([10, 0, 100])
        high_yellow = np.array([40, 255, 255])
        # Create masks for white and yellow colors
        white_mask = cv2.inRange(hls, low_white, high_white)
        yellow_mask = cv2.inRange(hls, low_yellow, high_yellow)
        # Combine masks to get the final mask
        mask = cv2.bitwise_or(white_mask, yellow_mask)
        # Apply mask to the original image
        result = cv2.bitwise_and(image, image, mask=mask)
        return result

    def average_slope_intercept(self, lines, image):
        left_fit_new = []
        right_fit_new = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = lineOop #, it looks like the code got cut off. Here's the rest of it:

                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                intercept = parameters[1]
                if slope < 0:
                    right_fit_new.append((slope, intercept))
                else:
                    left_fit_new.append((slope, intercept))

        if left_fit_new:
            left_fit_avg = np.average(left_fit_new, axis=0)
            if self.left_fit is None:
                self.left_fit = left_fit_avg
            else:
                self.left_fit = 0.9 * self.left_fit + 0.1 * left_fit_avg
        if right_fit_new:
            right_fit_avg = np.average(right_fit_new, axis=0)
            if self.right_fit is None:
                self.right_fit = right_fit_avg
            else:
                self.right_fit = 0.9 * self.right_fit + 0.1 * right_fit_avg

        if self.left_fit is not None and self.right_fit is not None:
            left_slope, left_intercept = self.left_fit
            right_slope, right_intercept = self.right_fit
            y1 = image.shape[0]
            y2 = int(y1 * 0.6)
            left_x1 = int((y1 - left_intercept) / left_slope)
            left_x2 = int((y2 - left_intercept) / left_slope)
            right_x1 = int((y1 - right_intercept) / right_slope)
            right_x2 = int((y2 - right_intercept) / right_slope)
            left_line = np.array([[[left_x1, y1, left_x2, y2]]], dtype=np.int32)
            right_line = np.array([[[right_x1, y1, right_x2, y2]]], dtype=np.int32)
            self.num_left_lines = len(left_fit_new)
            self.num_right_lines = len(right_fit_new)
            self.left_fit = (left_slope, left_intercept)
            self.right_fit = (right_slope, right_intercept)
            self.draw_lines(image, [left_line, right_line], thickness=5)

    def canny(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny

    def region_of_interest(self, image):
        height = image.shape[0]
        width = image.shape[1]
        vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32)
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, vertices, 255)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image

    def draw_lines(self, image, lines, color=[0, 255, 0], thickness=2):
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)

    def pid_controller(self, left, right):
        error = right - left
        k_p = 0.5
        k_d = 0.1
        k_i = 0.1
        pid_output = k_p * error + k_d * (error - self.prev_error) + k_i * self.integral_error
        self.prev_error = error
        self.integral_error += error
        return pid_output

ld = LaneDetection()