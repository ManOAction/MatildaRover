"""
This is hardware test for the motors.

Working voltage: 9V
Working current: 1.2A

"""

from gpiozero import Motor
from time import sleep


MotorSpeed = float(".3")

RMotor = Motor(13, 6)
LMotor = Motor(19, 26)


def stop_all():
    RMotor.stop()
    LMotor.stop()


def motor_test(motorName):
    if motorName == "RMotor":
        print("Testing right motor....")
        RMotor.forward(MotorSpeed)
        print("Forward")
        sleep(2)
        RMotor.backward(MotorSpeed)
        print("Backward")
        sleep(2)
        RMotor.stop()
    elif motorName == "LMotor":
        print("Testing left motor....")
        LMotor.forward(MotorSpeed)
        print("Forward")
        sleep(2)
        LMotor.backward(MotorSpeed)
        print("Backward")
        sleep(2)
        LMotor.stop()
    elif motorName == "Both":
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

    stop_all()

    return True


def main():

    stop_all()

    options = [(1, "RMotor"), (2, "LMotor"), (3, "Both"), (4, "Exit")]

    while True:
        print("Choose the motor you want to test: ")
        for option in options:
            print(f"{option[0]}. {option[1]}")
        motorName = input("Enter Option Number: ")
        motorName = int(motorName)
        motorName = options[motorName - 1][1]

        if motorName == "Exit":
            break

        motor_test(motorName)

    print("Exiting....")


if __name__ == "__main__":
    main()
