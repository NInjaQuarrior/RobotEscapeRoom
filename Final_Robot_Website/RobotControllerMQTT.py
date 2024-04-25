import paho.mqtt.client as mqtt
import keyboard


client = mqtt.Client(client_id="Robot_Controller")
mqtt_address = '192.168.1.6'

motionTopic = "robot/motion"
cameraTopic = "robot/util/camera"
armTopic = "robot/util/arm"
blckLightTopic = "robot/util/black"
ledTopic = "robot/util/led"


status = "stop"
def mqtt_setup():
    client.connect(mqtt_address, 1883)
    print("connected")

class Commands:
    def __init__(self):
        self.status = "stop"
        self.camStatus = "stop"
        self.LEDStatus = "off"
        self.BlackStatus = "off"

com  = Commands()

def sendForward(self):
    if com.status != "for":
        print("sending Forward")
        client.publish(motionTopic,payload="for")
        com.status = "for"

def sendStop(self):
    if com.status != "stop":
        print("sending stop")
        client.publish(motionTopic,payload="stop")
        com.status = "stop"

def sendBack(self):
    if com.status != "back":
        print("sending back")
        client.publish(motionTopic,payload="back")
        com.status = "back"

def sendLeft(self):
    if com.status != "left":
        print("sending left")
        client.publish(motionTopic,payload="left")
        com.status = "left"

def sendRight(self):
    if com.status != "right":
        print("sending right")
        client.publish(motionTopic,payload="right")
        com.status = "right"

def sendUp(self):
    if com.camStatus != "up":
        print("sending up")
        client.publish(cameraTopic,payload="up")
        com.status = "up"

def sendDown(self):
    if com.camStatus != "down":
        print("sending down")
        client.publish(cameraTopic,payload="down")
        com.status = "down"
def sendCamStop(self):
    if com.camStatus != "stop":
        print("sending stop")
        client.publish(cameraTopic,payload="stop")
        com.status = "stop"

def sendArmUp(self):
    if com.camStatus != "armup":
        print("sending armup")
        client.publish(armTopic,payload="armup")
        com.status = "armup"

def sendArmDown(self):
    if com.camStatus != "armdown":
        print("sending armdown")
        client.publish(armTopic,payload="armdown")
        com.status = "armdown"
def sendArmStop(self):
    if com.camStatus != "armstop":
        print("sending armstop")
        client.publish(armTopic,payload="armstop")
        com.status = "armstop"

def toggleLED(self):
    if com.LEDStatus == "off":
        print("sending on")
        client.publish(ledTopic,payload="on")
        com.LEDStatus = "on"
    else:
        print("sending off")
        client.publish(ledTopic,payload="off")
        com.LEDStatus = "off"

def toggleBlack(self):
    if com.BlackStatus == "off":
        print("sending on")
        client.publish(blckLightTopic,payload="on")
        com.BlackStatus = "on"
    else:
        print("sending off")
        client.publish(blckLightTopic,payload="off")
        com.BlackStatus = "off"


def setUpBinds():
        #forward
        keyboard.on_press_key("w",sendForward)
        keyboard.on_release_key("w",sendStop)
        keyboard.on_press_key("up",sendForward)
        keyboard.on_release_key("up",sendStop)

        #backward
        keyboard.on_press_key("s",sendBack)
        keyboard.on_release_key("s",sendStop)
        keyboard.on_press_key("down",sendBack)
        keyboard.on_release_key("down",sendStop)

        #right
        keyboard.on_press_key("d",sendRight)
        keyboard.on_release_key("d",sendStop)
        keyboard.on_press_key("right",sendRight)
        keyboard.on_release_key("right",sendStop)

        #left
        keyboard.on_press_key("a",sendLeft)
        keyboard.on_release_key("a",sendStop)
        keyboard.on_press_key("left",sendLeft)
        keyboard.on_release_key("left",sendStop)

        #camera up
        keyboard.on_press_key("e",sendUp)
        keyboard.on_release_key("e",sendCamStop)
        

        #camera down
        keyboard.on_press_key("q",sendDown)
        keyboard.on_release_key("q",sendCamStop)

        #arm up
        keyboard.on_press_key("r",sendArmUp)
        keyboard.on_release_key("r",sendArmStop)
        
        #arm down
        keyboard.on_press_key("f",sendArmDown)
        keyboard.on_release_key("f",sendArmStop)

        #toggle led
        keyboard.on_press_key("l",toggleLED)

        #toggle blacklight
        keyboard.on_press_key("b",toggleBlack)

def runControls():
    mqtt_setup()
    #com = Commands()
    setUpBinds()
    keyboard.wait()
        
if __name__ == '__main__':
	runControls()