"""
Tests fpr Si7021 sensor breakout board.
"""

import board
from busio import I2C
from adafruit_si7021 import SI7021


i2c = I2C(board.SCL, board.SDA)
AtmoSensor = SI7021(i2c)


def report_atmo():
    print("The Temperature: %0.1f F" % (AtmoSensor.temperature * (9 / 5) + 32))
    print("Humidity: %0.1f %%" % AtmoSensor.relative_humidity)

    return True


report_atmo()


print("Testing complete")
