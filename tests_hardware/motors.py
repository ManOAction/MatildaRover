"""
This is hardware test for the motors.

Working voltage: 9V
Working current: 1.2A

"""

from gpiozero import LED, Motor
from time import sleep


MotorSpeed = float(".3")

RMotor = Motor(13, 6)
LMotor = Motor(19, 26)

print("Testing right motor....")
RMotor.forward(MotorSpeed)
print("Forward")
sleep(2)
RMotor.backward(MotorSpeed)
print("Backward")
sleep(2)
RMotor.stop()

print("Testing left motor....")
LMotor.forward(MotorSpeed)
print("Forward")
sleep(2)
LMotor.backward(MotorSpeed)
print("Backward")
sleep(2)
LMotor.stop()

print("Testing both motors....")
RMotor.forward(MotorSpeed)
LMotor.forward(MotorSpeed)
print("Forward")
sleep(2)
RMotor.backward(MotorSpeed)
LMotor.backward(MotorSpeed)
print("Backward")
sleep(2)
RMotor.stop()
LMotor.stop()

print("Motors at rest...")
sleep(5)

print("Testing complete")
