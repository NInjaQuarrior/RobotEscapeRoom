import network
import socket
from time import sleep
import machine
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import ubinascii
from picozero import Button


class MyMotor:
    def __init__(self):
        self.PWMA = PWM(Pin(15))
        self.AIN2 = Pin(14, Pin.OUT)
        self.AIN1 = Pin(13, Pin.OUT)
        self.PWMA.freq(60)
        self.fullSpeed = 65535
        self.STBY = Pin(12, Pin.OUT)

        self.STBY.high()#enable the motor STBY must be kept at high
    
    def reverse(self,speed):
        self.AIN1.high()
        self.AIN2.low()
        self.PWMA.duty_u16(int(speed*self.fullSpeed))
    
    def forward(self,speed):
        self.AIN1.low()
        self.AIN2.high()
        self.PWMA.duty_u16(int(speed*self.fullSpeed))
        
    def stop(self):
        self.AIN1.low()
        self.AIN2.low()
    
    def forwardTime(self,speed, time):
        self.forward(speed)
        sleep(time)
        self.stop()
        
    def reverseTime(self, speed, time):
        self.reverse(speed)
        sleep(time)
        self.stop()

        
class MQTTController:
    def __init__(self):
        self.isSetup = False
        self.waitingForPuzzle = True
        self.waitingOnButton = True
        
        #self.controlsSwitch = False
        
        self.pico_id = 'Motor1'
        self.topic = 'room'
        
        self.switchID = 0
        #self.switchPin = 18
        self.switch = Pin(18, Pin.IN, Pin.PULL_DOWN)
        
        self.ledType = 0
        
        self.ee_type = 'Motor'
        
        self.led = Pin("LED", Pin.OUT)
        self.led.off()

        self.ssid = "escaperoom"
        self.password = None

        self.mqtt_server = '192.168.1.2'
        self.client_id = 'Door1'

        self.client = MQTTClient(self.client_id, self.mqtt_server)

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
        print("MQTT Connected")
        self.led.on()

    def setup(self):
        self.connect() # connect wifi and MQTT
    #take message in order "switchID,ledType"
    def determineType(self,topic, msg):
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        split = msg.split(',')
        
        self.switchID = split[0]
        self.ledType = split[1]
        
        
        dMSG = 'connected:' + self.pico_id + ','+ self.ee_type + ',' + self.switchID + ',' + self.ledType
        
        self.client.publish(self.topic + "/setup/"+ self.pico_id + "/status", dMSG)
        self.isSetup = True
        print(self.isSetup)
        
    #message is "OPEN" or "CLOSE"
    def motorCallback2(self, topic, msg):
        motor = MyMotor()
        
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        
        if msg == "OPEN":
            print("dunno how to open a door")
            #TODO open door call: forwardTime(someVal, someOtherVal)
        elif msg == "CLOSE":
            print("dunno how to close a door")
            #TODO close door call: reverseTime(someVal, someOtherVal)
        #potential TODO door speed input & accomodating math?
            
        self.waitingForPuzzle = False
    #take message in order "move_type,speed,time"
    def motorCallback(self,topic, msg):
        motor = MyMotor()
        
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        
        split = msg.split(',')
        
        move_type = split[0]
        speed = float(split[1])
        time = int(split[2])
        #TODO add feature to come back and stop, ie multiple cues to one controller
        if move_type == "forward":
            motor.forward(speed)
        elif move_type == "reverse":
            motor.reverse(speed)
        elif move_type == "forwardTime":
            print(speed)
            print(time)
            motor.forwardTime(speed, time)
        elif move_type == "reverseTime":
            motor.reverseTime(speed, time)
            
        self.waitingForPuzzle = False
          
    #def servoCallback(self,topic, msg):
        
    def buttonPressed(self):
        dMSG= "True"
        self.client.publish(self.topic + '/switch'+ self.switchID, dMSG)
        
    def run(self):
        self.setup()
        self.client.set_callback(self.determineType)
        while self.isSetup is False:
            self.client.subscribe(self.topic + '/setup/' + self.pico_id)
            sleep(1)
            #print(self.isSetup)
        #print("out of loop1")
        if self.ee_type == "Motor":
            print("set call motor")
            self.client.set_callback(self.motorCallback2)
        elif self.ee_type == "Servo":
            print("set call servo")
            self.client.set_callback(self.servoCallback)
            
        if self.switchID is not '0':
            dMSG= "False"
            self.client.publish(self.topic + '/switch'+ self.switchID, dMSG)
            print("Switch Connected")
            
            
        
        while self.waitingForPuzzle or self.waitingOnButton is True:
            if self.waitingForPuzzle is True:
                #print("waiting on: " + self.topic + '/puzzle' + self.puzzle_num)
                self.client.subscribe(self.topic + '/' + self.pico_id)
            if self.waitingOnButton is True:
                if self.switch.value():
                    self.buttonPressed()
                    self.waitingOnButton = False 
                
            
                
        
    
controller = MQTTController()
controller.run()
