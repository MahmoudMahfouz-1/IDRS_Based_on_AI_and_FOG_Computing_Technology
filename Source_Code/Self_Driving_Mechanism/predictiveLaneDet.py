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
        self.cap.set(3, 320)  # Set frame width
        self.cap.set(4, 240)  # Set frame height
        self.red = False
        self.num_left_lines = 0
        self.num_right_lines = 0
        self.prev_lane_params = None
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

                    if self.prev_lane_params is not None:
                        predicted_lines = self.predict_lines(lines)
                        lines = np.concatenate((lines, predicted_lines))

                    self.average_slope_intercept(lines, lane_image)
                    line_image = self.display_lines(lines, lane_image)
                    lane_image = cv2.addWeighted(lane_image, 1, line_image, 1, 0)

                    cv2.imshow('frame', lane_image)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break

                    # Rest of the code for autonomous driving
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

        finally:
            self.cap.release()
            cv2.destroyAllWindows()

    def check_for_red(self, image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
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
        return image, status

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

        left_fit_avg = np.mean(left_fit, axis=0) if len(left_fit) > 0 else None
        right_fit_avg = np.mean(right_fit, axis=0) if len(right_fit) > 0 else None

        self.prev_lane_params = (left_fit_avg, right_fit_avg)

        if left_fit_avg is not None:
            self.num_left_lines += 1
            self.draw_lane_line(image, left_fit_avg, color=(0, 255, 0))

        if right_fit_avg is not None:
            self.num_right_lines += 1
            self.draw_lane_line(image, right_fit_avg, color=(0, 255, 0))

    def draw_lane_line(self, image, line_params, color=(255, 0, 0), thickness=5):
        slope, intercept = line_params
        y1 = image.shape[0]
        y2 = int(y1 - 120)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)

    def canny(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny

    def region_of_interest(self, image):
        height, width = image.shape[:2]
        vertices = np.array([[(100, height), (width-100, height), (width-100, height-120), (100, height-120)]], dtype=np.int32)
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, vertices, 255)
        return cv2.bitwise_and(image, mask)

    def display_lines(self, lines, image):
        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                if len(line) > 0:
                    x1, y1, x2, y2 = line.reshape(4)
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        return line_image

    def predict_lines(self, lines):
        predicted_lines = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            slope, intercept = self.prev_lane_params
            predicted_x1 = x1 - 1  # Modify based on the desired prediction
            predicted_y1 = int(slope * predicted_x1 + intercept)
            predicted_x2 = x2 - 1  # Modify based on the desired prediction
            predicted_y2 = int(slope * predicted_x2 + intercept)
            predicted_lines.append([[predicted_x1, predicted_y1, predicted_x2, predicted_y2]])
        return np.array(predicted_lines)

if __name__ == '__main__':
    LaneDetection()

