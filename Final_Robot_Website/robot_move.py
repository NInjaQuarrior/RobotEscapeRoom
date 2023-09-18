"""
    File Created By: Liang Lu 
    File Created On: Feb. 26, 2023 
    Description: 
        this files stores the moving functions for our robot 
"""
# import built-in libraries
import RPi.GPIO as GPIO
from time import sleep
# import customized files
import robot_variables as rvars


# --- Robot Wheels Setup (Move Functions) ---
def right_forward():
    GPIO.output(rvars.motor_rA, GPIO.LOW)
    GPIO.output(rvars.motor_rB, GPIO.HIGH)
    GPIO.output(rvars.pwmR_out, GPIO.HIGH)


def right_backward():
    GPIO.output(rvars.motor_rA, GPIO.HIGH)
    GPIO.output(rvars.motor_rB, GPIO.LOW)
    GPIO.output(rvars.pwmR_out, GPIO.HIGH)


def left_forward():
    GPIO.output(rvars.motor_lA, GPIO.HIGH)
    GPIO.output(rvars.motor_lB, GPIO.LOW)
    GPIO.output(rvars.pwmL_out, GPIO.HIGH)


def left_backward():
    GPIO.output(rvars.motor_lA, GPIO.LOW)
    GPIO.output(rvars.motor_lB, GPIO.HIGH)
    GPIO.output(rvars.pwmL_out, GPIO.HIGH)


def stop():  # stop robot
    # Stop Right
    GPIO.output(rvars.motor_rA, GPIO.LOW)
    GPIO.output(rvars.motor_rB, GPIO.LOW)
    GPIO.output(rvars.pwmR_out, GPIO.LOW)
    # Stop Left
    GPIO.output(rvars.motor_lA, GPIO.LOW)
    GPIO.output(rvars.motor_lB, GPIO.LOW)
    GPIO.output(rvars.pwmL_out, GPIO.LOW)
    # print("Stop")


def move_forward():  # move robot forward
    right_forward()
    left_forward()
    # print("Going forwards")


def move_backward():  # move robot backward
    right_backward()
    left_backward()
    # print("Going backwards")


def turn_left():  # move robot left
    right_backward()
    left_forward()
    # print("Turning left")


def turn_right():  # move robot right
    right_forward()
    left_backward()
    # print("Turning right")

# --- Robot Wheels Setup (Move Functions) Ends ---


# --- Robot Servo Setup ---
"""
servo/camera home position: duty = 2.5 
servo/camera looking straight up (90/neutral): duty = 7.5 
"""


def servo_contraint(duty):
    if (duty < 2.5):
        duty = 2.5
    elif (duty > 7.5):
        duty = 7.5
    return duty
# --- Robot Servo Setup Ends ---


# --- Robot Arm Setup ---
def enable_arm():
    pass

# --- Robot Arm Setup Ends ---


# --- Robot LED Setup ---
def led_on():
    GPIO.output(rvars.led_pin, GPIO.HIGH)


def led_off():
    GPIO.output(rvars.led_pin, GPIO.LOW)


def blacklight_on():
    GPIO.output(rvars.blacklight_pin, GPIO.HIGH)


def blacklight_off():
    GPIO.output(rvars.blacklight_pin, GPIO.LOW)

# --- Robot LED Setup Ends ---
