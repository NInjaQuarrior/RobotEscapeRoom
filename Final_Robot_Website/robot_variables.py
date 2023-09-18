"""
    File Created By: Liang Lu 
    File Created On: Feb. 26, 2023 
    Description: 
        this files stores the global variables for the robot 
"""

# Pins for Motor Driver Inputs
motor_rA = 5        # GPIO3; output pin
motor_rB = 3        # GPIO2; output pin
motor_lA = 16       # GPIO23; output pin
motor_lB = 18       # GPIO24; output pin

# Other Pins
motor_rtxd = 8      # GPIO14 (TXD); input pin
motor_rrxd = 10     # GPIO15 (RXD); input pin
motor_ltxd = 31     # GPIO6; input pin
motor_lrxd = 29     # GPIO5; input pin

# PWM Pins
pwmR_out = 32       # GPIO12 (PWM0)
pwmL_out = 33       # GPIO13 (PWM1)

# Other Pins
servo_pin = 36      # GPIO16
led_pin = 11        # GPIO17
blacklight_pin = 13  # GPIO27

# put pins into list for setup()
input = [motor_rtxd, motor_rrxd, motor_ltxd, motor_lrxd]
output = [motor_rA, motor_rB, motor_lA, motor_lB,
          pwmR_out, pwmL_out, servo_pin, led_pin, blacklight_pin]
