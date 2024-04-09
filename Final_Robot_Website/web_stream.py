# Import necessary libraries
from flask import Flask, render_template, redirect, request, url_for, session, send_file, Response
from flask_session import Session
import cv2
import os
import paho.mqtt.client as mqtt

# Initialize the Flask app
app = Flask(__name__)
camera = cv2.VideoCapture(0)
scan_enabled = False

Session(app)
app.secret_key = 'RobotEscapeRoomMQP2324'

#import puzzle script (from upload file later on?)
from puzzleProgression import testMQTT, runMQTT


# --- MQTT Setup ---

pi_ip_address = '192.168.1.33'
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
    client.subscribe("robot/  function")
    # client.subscribe("robot/puzzle")
    client.loop_start()

# --- MQTT Setup Ends ---

# --- Flask templates ---
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/loadScript', methods=['GET', 'POST'])
def loadScript():
    file_content = session.get('file_content', '')

    if request.method == 'POST':
        if 'fileInput' not in request.files:
            return 'No file part'

        file = request.files['fileInput']

        if file.filename == '':
            return 'No selected file'

        file_content = file.read().decode('utf-8')

        session['file_content'] = file_content
        
        print("File Content:")
        print(file_content)

    return render_template('loadScript.html', file_content=file_content)

@app.route('/')
@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/end_page')
def end_page():
    return render_template('endPage.html')


@app.route('/manual')
def manual():
    return render_template('manual.html')


@app.route('/win')
def win():
    return render_template('win.html')
# --- Flask templates Ends ---


if __name__ == "__main__":
    mqtt_setup()
    # testMQTT(client)
    runMQTT(client)
    app.run(host='0.0.0.0', port=8000, debug=False)
    # with open("Final_Robot_Website/RobotControllerMQTT.py") as file:
    #     exec(file.read())
