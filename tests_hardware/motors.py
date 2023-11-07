"""
This is hardware test for the motors.

Working voltage: 9V
Working current: 1.2A

"""

from gpiozero import LED, Motor
from time import sleep


MotorSpeed = float(".5")

MotorWake = LED(17)
MotorWake.off()

RMotor = Motor(13, 6)
LMotor = Motor(19, 26)

print("Testing right motor....")
RMotor.forward(MotorSpeed)
print("Forward")
sleep(2)
RMotor.backward(MotorSpeed)
print("Backward")
sleep(2)

print("Testing left motor....")
LMotor.forward(MotorSpeed)
print("Forward")
sleep(2)
LMotor.backward(MotorSpeed)
print("Backward")
sleep(2)

print("Testing both motors....")
RMotor.forward(MotorSpeed)
LMotor.forward(MotorSpeed)
print("Forward")
sleep(2)
RMotor.backward(MotorSpeed)
LMotor.backward(MotorSpeed)
print("Backward")
sleep(2)

print("Testing complete")
