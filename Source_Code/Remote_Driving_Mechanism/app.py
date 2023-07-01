from flask import Flask, render_template, Response, request, jsonify
import RPi.GPIO as GPIO
import cv2
import time
import control2 as ctrl


motorSpeed = 100 # Maximum 100 
app = Flask(__name__)

# Define the route for the web page
# Replace with the actual filename of your HTML template

# Define the route for receiving control commands

cap= cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Flask route for video stream
@app.route('/video_feed')
def video_feed():
   return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

        # Flask route for control buttons
@app.route('/control', methods=['POST'])
def control():
    command = request.form['command']
    value = request.form['value']
    # Perform action based on the received command and value
    if command == 'backward':
        if value == 'true':
            # Code to make the RC car move forward untill button release
            ctrl.backward(motorSpeed)
        else:
            # Code to stop the RC car from moving backward
            ctrl.stop()
    elif command == 'forward':
        if value == 'true':
            # Code to make the RC car move forward untill button release
            ctrl.forward(motorSpeed)
        else:
            # Code to stop the RC car from moving backward
            ctrl.stop()
    elif command == 'left':
        if value == 'true':
            print(value)
            ctrl.turnLeft(motorSpeed)
        else:
            print(value)
            ctrl.stop()
               
    elif command == 'right':
       if value == 'true':
            ctrl.turnRight(motorSpeed)
       else:
            ctrl.stop()
    elif command == 'stop':
        if value == 'true':
            ctrl.stop()
        else:
            ctrl.stop()

    return 'OK',200
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)