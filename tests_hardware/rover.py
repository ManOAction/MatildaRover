"""This is the central rover behavior script.  This holds the behavior for
roving =and basic UI.

# changelog
2020-02-15, JDL: Creating stable loops and move commands
2019-11-24, JDL: First draft.


# Dependencies

Blinka Library
-------------
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
sudo pip3 install adafruit-blinka -U

busio
board
adafruit_fxos8700
adafruit_fxas21002c
adafruit_si7021
------------

Bluetin Echo
------------
https://github.com/MarkAHeywood/Bluetin_Python_Echo
sudo pip3 install Bluetin_Echo -U

Bluetin_Echo
------------

"""

from gpiozero import LED, Motor
from time import sleep


# These are the Blinka tools for managing the related sensors
from busio import I2C
import board
from adafruit_fxos8700 import FXOS8700  # accelo / magnetometer
from adafruit_fxas21002c import FXAS21002C  # gyro
from adafruit_si7021 import SI7021  # temp and humidiy
from Bluetin_Echo import Echo  # HCSR04 Module Uses BCM Pins!


# Constants (move externaly to a config when you have time)
####################################################
NinetyDegreeTime = float('.65')
OneEightyDegreeTime = float('1.3')
RightTurnMod = float('1')  # float('1.109')
MotorSpeed = float('.8')

mag_offset_x = float('25')
mag_offset_y = float('-28')
mag_offset_z = float('-85')

####################################################

# Sensing
####################################################


def report_atmo():
    print("The Temperature: %0.1f F" % (AtmoSensor.temperature*(9/5)+32))
    print("Humidity: %0.1f %%" % AtmoSensor.relative_humidity)

    return True


def report_dist():
    samples = 3
    i = 0
    while i < 20:
        d = LeftEye.read('cm', samples)
        print('Left: ', d, 'cm')
        d = RightEye.read('cm', samples)
        print('Right: ', d, 'cm')
        sleep(.25)
        i += 1

    return True


# ___  ___                                    _
# |  \/  |                                   | |
# | .  . | _____   _____ _ __ ___   ___ _ __ | |_
# | |\/| |/ _ \ \ / / _ \ '_ ` _ \ / _ \ '_ \| __|
# | |  | | (_) \ V /  __/ | | | | |  __/ | | | |_
# \_|  |_/\___/ \_/ \___|_| |_| |_|\___|_| |_|\__|
#################################################


def move_forward(MoveTime):
    print('Moving forward.')
    MotorWake.on()
    RMotor.forward(MotorSpeed)
    LMotor.forward(MotorSpeed)
    sleep(MoveTime)
    RMotor.stop()
    LMotor.stop()
    MotorWake.off()
    print('End moving forward.')
    return True


def move_reverse(MoveTime):
    print('Moving backwards.')
    MotorWake.on()
    RMotor.backward(MotorSpeed)
    LMotor.backward(MotorSpeed)
    sleep(MoveTime)
    RMotor.stop()
    LMotor.stop()
    MotorWake.off()
    return True


def move_turnleft(MoveTime):
    print('Turning left.')
    MotorWake.on()
    RMotor.forward(MotorSpeed)
    LMotor.backward(MotorSpeed)
    sleep(MoveTime)
    RMotor.stop()
    LMotor.stop()
    MotorWake.off()
    return True


def move_turnright(MoveTime):
    print('Turning right.')
    MotorWake.on()
    RMotor.backward(MotorSpeed)
    LMotor.forward(MotorSpeed)
    sleep(MoveTime*RightTurnMod)
    RMotor.stop()
    LMotor.stop()
    MotorWake.off()
    return True


# Patterns
##############################################
def move_box(MoveTime):
    move_forward(MoveTime)
    move_turnleft(NinetyDegreeTime)
    move_forward(MoveTime)
    move_turnleft(NinetyDegreeTime)
    move_forward(MoveTime)
    move_turnleft(NinetyDegreeTime)
    move_forward(MoveTime)
    move_turnleft(NinetyDegreeTime)


def findpath(direction):

    dL = 1
    dR = 1
    while (dR == 0 or dL <= 80) and (dR == 0 or dR <= 80):
        if direction == 'left':
            move_turnleft(float(.1))
        elif direction == 'right':
            move_turnright(float(.1))
        else:
            print('Impossible directon parameter.')
            raise ValueError

        sleep(.5)
        dL = LeftEye.read('cm', 3)
        dR = RightEye.read('cm', 3)

    return True


def move_hunt():
    objectfound = 0
    dL = LeftEye.read('cm', 5)
    dR = RightEye.read('cm', 5)
    while objectfound < 100:
        MotorWake.on()
        RMotor.forward(float(MotorSpeed*.2))
        LMotor.forward(float(MotorSpeed*.2))
        print('Moving Forward...')
        dL = 0
        dR = 0

        while (dL == 0 or dL > 40) and (dR == 0 or dR > 40):
            dL = LeftEye.read('cm', 3)
            print('Left ', dL, 'cm')
            dR = RightEye.read('cm', 3)
            print('Right ', dR, 'cm')

        RMotor.stop()
        LMotor.stop()
        MotorWake.off()
        print('Object Found!')
        objectfound += 1
        sleep(.5)
        # print('Reversing...')
        # move_reverse(float(.3))
        # sleep(1)
        print('Turning...')
        print(f'Right eye distance was {dR}.')
        if (int(dR) % 2) == 0:
            print(f"""That's an even number, so I'm turning right.""")
            findpath('right')
        else:
            print(f"""That's an odd number, so I'm turning left.""")
            findpath('left')



# ______
# | ___ \
# | |_/ /_____   _____ _ __
# |    // _ \ \ / / _ \ '__|
# | |\ \ (_) \ V /  __/ |
# \_| \_\___/ \_/ \___|_|
#################################################
def display_options():
    print("""

    #############
    x for exit
    wasd keys for directional controls. Capital letters for custom turns.
    c for 180
    b for Box Pattern

    r for Atmospheric Report
    p for Distance Sensing Mode
    h for Hunt Mode
    #############

    """)

    return True


def rover_initialize():

    global RMotor, LMotor, MotorWake, AtmoSensor, LeftEye, RightEye, Accelo, Gyro

    # Initializing I2C for sensors
    i2c = I2C(board.SCL, board.SDA)

    # Initializing Gyro and Magnetometer
    Accelo = FXOS8700(i2c)
    Gyro = FXAS21002C(i2c)

    # Initializing Atmo Sensor
    AtmoSensor = SI7021(i2c)

    # Annoyingly it looks like the HCSR04 Libary uses DPI Pin Numbering instead
    # of Broadcom.  Check here https://pinout.xyz/pinout/pin18_gpio24
    # Read about speed of sound calibration in doc
    # BCM 23 & 24 are DPI 19 and 20
    LeftEye = Echo(23, 24)
    RightEye = Echo(17, 27)

    MotorWake = LED(17)
    MotorWake.off()

    # Args are GPIO Pins for forward, backward, and motor controller sleep
    RMotor = Motor(13, 6)  # Motor(19, 26, 13)
    LMotor = Motor(19, 26)  # Motor(20, 21, 13)

    return True


def rover_loop():

    rover_quit = False

    while rover_quit is not True:

        display_options()

        print('What is thy bidding, master?')
        user_input = input()

        try:
            # Core Commands
            ######################
            if user_input == 'x':
                return False

            if user_input == 'w':
                print('For how many seconds?')
                move_forward(float(input()))

            if user_input == 'a':
                print('90 Time is set to {0}'.format(NinetyDegreeTime))
                move_turnleft(float(NinetyDegreeTime))

            if user_input == 'A':
                print('For how many seconds?')
                move_turnleft(float(input()))

            if user_input == 's':
                print('For how many seconds?')
                move_reverse(float(input()))

            if user_input == 'd':
                move_turnright(float(NinetyDegreeTime))

            if user_input == 'D':
                print('For how many seconds?')
                move_turnright(float(input()))

            if user_input == 'c':
                print('180 Time is set to {0}'.format(OneEightyDegreeTime))
                move_turnleft(float(OneEightyDegreeTime))

            if user_input == 'b':
                print('How big a box?')
                move_box(float(input()))

            if user_input == 'r':
                report_atmo()

            if user_input == 'p':
                report_dist()

            if user_input == 'h':
                move_hunt()

        except Exception as errormessage:
            print('Problem with user input...')
            print(errormessage)

        rover_quit = False

    return True


#  _____                    _
# |  ___|                  | |
# | |____  _____  ___ _   _| |_ ___
# |  __\ \/ / _ \/ __| | | | __/ _ \
# | |___>  <  __/ (__| |_| | ||  __/
# \____/_/\_\___|\___|\__,_|\__\___|
###############################################################################

if __name__ == '__main__':
    rover_initialize()
    rover_loop()

print('I think we\'re done here.')
