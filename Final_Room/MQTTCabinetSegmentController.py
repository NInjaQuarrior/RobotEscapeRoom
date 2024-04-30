import network
import socket
from time import sleep
import machine
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import ubinascii
from picozero import pico_led, Button, LED, DigitalLED

class MyServo:
    def __init__(self):
        self.MID = 1500000
        self.MIN = 1000000
        self.MAX = 2000000
        self.PinNum = 18
        
        self.pwm = PWM(Pin(self.PinNum))
        self.pwm.freq(50)
        
    def moveTo(self, position):
        if position is "MAX":
            self.pwm.duty_ns(self.MAX)
        elif position is "MID":
            self.pwm.duty_ns(self.MID)
        elif position is "MIN":
            self.pwm.duty_ns(self.MIN)
        elif position is "OPEN":
            self.pwm.duty_ns(2200000)
        elif position is "CLOSE":
            self.pwm.duty_ns(1200000)
        
class MQTTController:
    def __init__(self):
        self.isSetup = False
        self.waitingForPuzzle = True
        self.waitingOnButton = True
        
        self.pico_id = 'cabinet_0'
        self.topic = 'room'
        
        self.switchID = 0
        #self.switchPin = 18
        self.switch = Pin(18, Pin.IN, Pin.PULL_DOWN)
        
        self.ledType = 0
        
        self.ee_type = 'servo'

 
                        
        self.led = Pin("LED", Pin.OUT)
        self.led.off()
        
        self.ssid = "escaperoom"
        self.password = None

        self.mqtt_server = '192.168.1.6'

        self.client = MQTTClient(self.pico_id, self.mqtt_server)

    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        
        print(wlan.ifconfig())
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        print(mac)
        #connect MQTT
        self.client.connect()
        dMSG = 'waiting:' + self.pico_id + ',' + self.switchID + ',' + self.ledType
        self.client.publish(self.topic + "/setup/"+ self.pico_id + "/status", dMSG)
        self.led.on()

    def setup(self):
        self.connect() # connect wifi and MQTT
    #take message in order "puzzle_num,switchID"
    def getPeripherals(self,topic, msg):
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        split = msg.split(',')
        
        self.switchID = split[0]
        self.ledType = split[1]

        dMSG = 'playing:' + self.pico_id + ',' + self.switchID + ',' + self.ledType
        
        self.client.publish(self.topic + "/setup/"+ self.pico_id + "/status", dMSG)
        self.isSetup = True
        print(self.isSetup)
                
    def servoCallback(self,topic, msg):
        servo = MyServo()
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        
        split = msg.split(',')
        
        targetPos = split[0]
        
        servo.moveTo(targetPos)
            
        #self.waitingForPuzzle = False
        
    def buttonPressed(self):
        dMSG= "True"
        self.client.publish(self.topic + '/switch_'+ self.switchID, dMSG)
        
    def buttonReleased(self):
        dMSG= "False"
        self.client.publish(self.topic + '/switch_'+ self.switchID, dMSG)
        
    def run(self):
        self.setup()
        self.client.set_callback(self.getPeripherals)
        while self.isSetup is False:
            self.client.subscribe(self.topic + '/setup/' + self.pico_id)
            sleep(1)

        print("set call servo")
        self.client.set_callback(self.servoCallback)
            
        if self.switchID is not '0':
            dMSG= "False"
            self.client.publish(self.topic + '/switch_'+ self.switchID, dMSG)
            print("Switch Connected")
        
        while True:
            #print("waiting on puzzle")
            if self.waitingForPuzzle is True:
                self.client.subscribe(self.topic + '/' + self.pico_id)
                
            if self.switch.value():
                self.buttonPressed()
            else:
                self.buttonReleased()
                    
                    #self.waitingOnButton = False 
                
            
controller = MQTTController()
controller.run()


