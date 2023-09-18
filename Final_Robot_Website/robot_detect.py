"""
    File Created By: Liang Lu
    File Created On: Mar. 25, 2023
    Description:
        this files uses the camera and detects for APRIL Tag
        aruco generator: https://chev.me/arucogen/
        https://www.youtube.com/watch?v=v5a7pKSOJd8
"""
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import os
from time import sleep
import paho.mqtt.client as mqtt


# --- MQTT Setup ---

pi_ip_address = 'mqtt.eclipseprojects.io'
client = mqtt.Client(client_id="robot_detect", clean_session=True)


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def on_message(client, userdata, msg):
    print("on_message | topic: "+msg.topic +
          " \tmsg: "+str(msg.payload.decode("utf-8")))


def mqtt_setup() -> mqtt:
    # client.on_connect = on_connect
    client.on_message = on_message
    client.connect(pi_ip_address)
    client.loop_start()

# --- MQTT Setup Ends ---


def loadAugImages(path):
    myList = os.listdir(path)
    numMarkers = len(myList)
    augDics = {}
    for imgPath in myList:
        key = int(os.path.splitext(imgPath)[0])
        imgAug = cv.imread(f'{path}/{imgPath}')
        augDics[key] = imgAug
    return augDics


def findArucoMarkers(img, markerSize=6, totalMarker=250, draw=True):
    # function to detect for aruco
    # default is set to 6x6, where there is a total of 250 combinations
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    # arucoDict = aruco.Dictionary_get(key)
    # arucoParam = aruco.DetectorParameters_create()
    # bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

    dictionary = cv.aruco.getPredefinedDictionary(key)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)
    bboxs, ids, rejected = detector.detectMarkers(img)

    # print(ids)

    # if draw == true, a box will be drawn around the code if detected
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)

    # return ids
    return [bboxs, ids]


def augmentAruco(bbox, id, img, imgAug, drawID=True):
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]

    h, w, c = imgAug.shape
    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv.findHomography(pts2, pts1)
    imgOut = cv.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
    cv.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    imgOut = img + imgOut

    # if drawID:
    # cv.putText(imgOut, str(id), tl,
    #            cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    return imgOut


def start():  # function to start the loop for detecting aruco
    mqtt_setup()
    cap = cv.VideoCapture(0)
    augDics = loadAugImages("static/AugImg")

    try:
        while True:
            ret, img = cap.read()
            # ids = findArucoMarkers(img)
            arucoFound = findArucoMarkers(img)

            if len(arucoFound[0]) != 0:
                for bbox, id in zip(arucoFound[0], arucoFound[1]):
                    if int(id) in augDics.keys():
                        img = augmentAruco(
                            bbox, id, img, augDics[int(id)], drawID=False)

            cv.imshow("image", img)
            cv.waitKey(1)

    except KeyboardInterrupt:
        print("destroying windows...")
        cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    start()
