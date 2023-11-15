"""
    File Created By: Liang Lu
    File Created On: Mar. 31, 2023
    Description:
        this files streams video to html
        aruco generator: https://chev.me/arucogen/
        https://www.youtube.com/watch?v=v5a7pKSOJd8
        https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
"""
# Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import cv2.aruco as aruco
import numpy as np
import os
import paho.mqtt.client as mqtt

# Initialize the Flask app
app = Flask(__name__)
camera = cv2.VideoCapture(0)
scan_enabled = False


# --- MQTT Setup ---

pi_ip_address = 'mqtt.eclipseprojects.io'
client = mqtt.Client(client_id="web_stream", clean_session=True)


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def on_message(client, userdata, msg):
    global scan_enabled
    print("on_message | topic: "+msg.topic +
          " \tmsg: "+str(msg.payload.decode("utf-8")))
    if (msg.topic == "robot/function"):
        if (msg.payload.decode("utf-8") == "enable scan"):
            scan_enabled = True
        elif (msg.payload.decode("utf-8") == "disable scan"):
            scan_enabled = False


def mqtt_setup() -> mqtt:
    client.connect(pi_ip_address)
    client.on_message = on_message
    client.subscribe("robot/function")
    # client.subscribe("robot/puzzle")
    client.loop_start()

# --- MQTT Setup Ends ---


def loadAugImages(path):  # loads image into dictionary
    myList = os.listdir(path)
    numMarkers = len(myList)
    # remove unneeded files from myList
    if '.DS_Store' in myList:
        myList.remove('.DS_Store')
    # add keys into library
    augDics = {}
    for imgPath in myList:
        key = int(os.path.splitext(imgPath)[0])
        imgAug = cv2.imread(f'{path}/{imgPath}')
        augDics[key] = imgAug
    return augDics


def findArucoMarkers(img, markerSize=6, totalMarker=250, draw=True):
    # function to detect for aruco
    # default is set to 6x6, where there is a total of 250 combinations
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    # for raspberry pi (three lines):
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(
        imgGray, arucoDict, parameters=arucoParam)

    # for testing (four lines); OpenCV 4.7.x:
    # dictionary = aruco.getPredefinedDictionary(key)
    # parameters = aruco.DetectorParameters()
    # detector = aruco.ArucoDetector(dictionary, parameters)
    # bboxs, ids, rejected = detector.detectMarkers(img)

    # look for aruco of id = 203 and send to broker
    if ids is not None and scan_enabled:
        for id in ids:
            if id == [203]:
                client.publish("robot/aruco", payload="aruco valid")

    # if draw == true, a box will be drawn around the code if detected
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)

    return [bboxs, ids]


def augmentAruco(bbox, id, img, imgAug, drawID=True):
    # overlay augmented image onto aruco
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]

    h, w, c = imgAug.shape
    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
    cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    imgOut = img + imgOut

    return imgOut


def gen_frames():
    # load image files into dictionary
    augDics = loadAugImages("static/AugImg")

    try:
        while True:
            success, frame = camera.read()  # read the camera frame
            # detect for aruco markers
            if not success:
                break
            else:
                arucoFound = findArucoMarkers(frame, draw=True)

            # overlay defined image onto aruco
            if len(arucoFound[0]) != 0:
                for bbox, id in zip(arucoFound[0], arucoFound[1]):
                    if int(id) in augDics.keys():
                        frame = augmentAruco(
                            bbox, id, frame, augDics[int(id)], drawID=False)

            # send frame to html
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # concat frame one by one and show result
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except KeyboardInterrupt:
        print("releasing cameras...")
        camera.release()
        client.disconnect()


# --- Flask templates ---
@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/end_page')
def end_page():
    return render_template('endPage.html')


@app.route('/hint')
def hint():
    return render_template('hint.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/intro')
def intro():
    return render_template('intro.html')


@app.route('/intro_redirect')
def intro_redirect():
    return render_template('intro_v2.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/manual')
def manual():
    return render_template('manual.html')


@app.route('/progress')
def progress():
    return render_template('progress.html')


@app.route('/rotate_puzzle')
def rotate_puzzle():
    return render_template('rotatePuzzle.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/win')
def win():
    return render_template('win.html')


@app.route('/manualv2')
def manualv2():
    return render_template('manualv2.html')
# --- Flask templates Ends ---


if __name__ == "__main__":
    mqtt_setup()
    app.run(host='0.0.0.0', port=8000, debug=False)
