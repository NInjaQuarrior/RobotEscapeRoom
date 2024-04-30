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
        
    def reverseTime(speed, time):
        self.reverse(speed)
        sleep(time)
        self.stop()

        
class MQTTController:
    def __init__(self):
        self.isSetup = False
        self.waitingForPuzzle = True
        self.waitingOnButton = True
        
        self.pico_id = 'door_0'
        self.topic = 'room'
        
        #setup switch
        self.switchID = 0     
        self.switch = Pin(18, Pin.IN, Pin.PULL_DOWN)
        
        self.ledType = 0
        
        self.ee_type = 'motor'
        
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

    #take message in order "switchID,ledType"
    def getPeripherals(self,topic, msg):
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        split = msg.split(',')
        
        self.switchID = split[0]
        self.ledType = split[1]
        
        
        dMSG = 'playing:' + self.pico_id + ','+ self.ee_type + ',' + self.switchID + ',' + self.ledType
        
        self.client.publish(self.topic + "/setup/"+ self.pico_id + "/status", dMSG)
        self.isSetup = True
        print(self.isSetup)
        
    #take message in order "move_type,speed,time"
    def motorCallback(self,topic, msg):
        motor = MyMotor()
        
        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')
        print(msg)
        
        split = msg.split(',')
        
        move_type = split[0]
        speed = float(split[1])
        time = float(split[2])

        if move_type == "forward":
            motor.forward(speed)
        elif move_type == "reverse":
            motor.reverse(speed)
        elif move_type == "forwardTime":
            motor.forwardTime(speed, time)
        elif move_type == "reverseTime":
            motor.reverseTime(speed, time)
        elif move_type == "open":
            motor.forwardTime(3.0,1.4)
        elif move_type == "close":
            motor.reverseTime(3.0,1.4)
            
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

        print("set call motor")
        self.client.set_callback(self.motorCallback)
            
        if self.switchID is not '0':
            dMSG= "False"
            self.client.publish(self.topic + '/Switch'+ self.switchID, dMSG)
            print("Switch Connected")
                
        while True:
            if self.waitingForPuzzle is True:
                self.client.subscribe(self.topic + '/' + self.pico_id)

            if self.switch.value():
                self.buttonPressed()
            else:
                self.buttonReleased()
                 
controller = MQTTController()
controller.run()
