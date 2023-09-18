"""
    File Created By: Liang Lu 
    File Created On: Mar. 21, 2023 
    Description: 
        this files takes in the keyboard control from local host 
"""

# import built-in libraries
import keyboard
import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
# import customized files
import robot_move as rmov
import robot_variables as rvars

# --- Global Variables ---
pi_ip_address = 'mqtt.eclipseprojects.io'
client = mqtt.Client(client_id="robot_control", clean_session=True)
servo = ""
puzzle = 1
enable_scan = False
enable_light = False
enable_blacklight = False
enable_move = False
duty = 2.5  # camera home position
# --- Global Variables Ends ---


# --- MQTT Setup ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def on_message(client, userdata, msg):
    global enable_move
    print("on_message | topic: "+msg.topic +
          " \tmsg: "+str(msg.payload.decode("utf-8")))
    # enable arm if puzzle 3 is completed.
    if (msg.topic == "website/status"):
        if msg.payload.decode("utf-8") == "puzzle 3 completed.":
            rmov.enable_arm()
    if (msg.topic == "robot/function"):
        if msg.payload.decode("utf-8") == "disable move":
            enable_move = False
        elif msg.payload.decode("utf-8") == "enable move":
            enable_move = True


def mqtt_setup() -> mqtt:
    client.connect(pi_ip_address)
    client.on_message = on_message
    client.subscribe("robot/function")
    client.subscribe("website/status")
    client.loop_start()

# --- MQTT Setup Ends ---


# --- Functions ---
def move_servo():  # FUNCION to move servo (for camera) up and down
    global servo, duty
    duty_stepper = 0.25
    if (keyboard.is_pressed("w")):      # move servo up
        duty = rmov.servo_contraint(duty+duty_stepper)
        servo.ChangeDutyCycle(duty)
        # sleep(0.2)
    elif (keyboard.is_pressed("s")):    # move servo down
        duty = rmov.servo_contraint(duty-duty_stepper)
        servo.ChangeDutyCycle(duty)
        # sleep(0.2)
    else:                               # stop servo from possible vibration
        servo.ChangeDutyCycle(0)
        # sleep(0.2)


def move_robot():  # FUNCIOM to control robot movement (wheels)
    if (keyboard.is_pressed("up")):         # move robot forward
        rmov.move_forward()
        sleep(0.2)
    elif (keyboard.is_pressed("down")):     # move robot backward
        rmov.move_backward()
        sleep(0.2)
    elif (keyboard.is_pressed("left")):     # turn robot left
        rmov.turn_left()
        sleep(0.2)
    elif (keyboard.is_pressed("right")):    # turn robot right
        rmov.turn_right()
        sleep(0.2)
    else:                                   # stop the robot
        rmov.stop()
        sleep(0.2)


def move_arm():
    pass


def robot_func():
    global enable_scan, enable_light, enable_blacklight
    if (keyboard.is_pressed("q") and not enable_scan):          # enable scanning
        client.publish("robot/function", payload="enable scan")
        enable_scan = True
        sleep(0.2)
    elif (keyboard.is_pressed("q") and enable_scan):            # disable scanning
        client.publish("robot/function", payload="disable scan")
        enable_scan = False
        sleep(0.2)
    elif (keyboard.is_pressed("l") and not enable_light):       # enable light
        client.publish("robot/function", payload="enable light")
        rmov.led_on()
        enable_light = True
        sleep(0.2)
    elif (keyboard.is_pressed("l") and enable_light):           # disable light
        client.publish("robot/function", payload="disable light")
        enable_light = False
        rmov.led_off()
        sleep(0.2)
    elif (keyboard.is_pressed("b") and not enable_blacklight):  # enable blacklight
        client.publish("robot/function", payload="enable blacklight")
        enable_blacklight = True
        rmov.blacklight_on()
        sleep(0.2)
    elif (keyboard.is_pressed("b") and enable_blacklight):      # disable blacklight
        client.publish("robot/function", payload="disable blacklight")
        enable_blacklight = False
        rmov.blacklight_off()
        sleep(0.2)


def puzzle_wizard():
    global puzzle
    if (keyboard.is_pressed("1")):
        puzzle = 1
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("2")):
        puzzle = 2
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("3")):
        puzzle = 3
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("4")):
        puzzle = 4
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("5")):
        puzzle = 5
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)

# --- Functions Ends ---


def setup():
    global servo, cam

    # RASPBERRY PI BOARD SETUP
    GPIO.setwarnings(False)
    # BOARD: uses pin numbers; BCM: uses GPIO numbers
    GPIO.setmode(GPIO.BOARD)
    # set input and output pins
    GPIO.setup(rvars.input, GPIO.IN)
    GPIO.setup(rvars.output, GPIO.OUT)

    # SERVO SET UP
    servo = GPIO.PWM(rvars.servo_pin, 50)  # for PWM with 50Hz
    servo.start(0)  # start servo
    servo.ChangeDutyCycle(duty)  # set servo/camera to home position
    sleep(0.5)
    servo.ChangeDutyCycle(0)  # stop servo (from possible vibration)
    print("camera to home position")

    # TURN LIGHTS OFF
    rmov.led_off()
    rmov.blacklight_off()

    # MQTT SET UP
    mqtt_setup()

    sleep(1)


def loop():
    if enable_move:
        move_servo()
        move_robot()
        robot_func()
    move_arm()
    # puzzle_wizard()


def destroy():
    print("stopping servo...")
    servo.stop()
    print("cleaning up...")
    GPIO.cleanup()
    print("disconnecting mqtt...")
    client.disconnect()


if __name__ == '__main__':     # Program start from here
    setup()
    while (1):
        try:
            loop()
            if (keyboard.is_pressed("esc")):
                client.publish("website/status", "escape")
                sleep(0.5)
                print("exiting...")
                break
        except KeyboardInterrupt:
            destroy()
