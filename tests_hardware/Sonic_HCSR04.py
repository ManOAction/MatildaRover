"""
Testsing the HCSR04 sensor
"""

from Bluetin_Echo import Echo  # HCSR04 Module Uses BCM Pins!
from time import sleep

# Annoyingly it looks like the HCSR04 Libary uses DPI Pin Numbering instead of Broadcom.
# Check here https://pinout.xyz/pinout/pin18_gpio24
# Read about speed of sound calibration in docs
# BCM 23 & 24 are DPI 19 and 20
LeftEye = Echo(23, 24)
RightEye = Echo(17, 27)


def report_dist():
    samples = 3
    i = 0
    while i < 20:
        d = LeftEye.read("cm", samples)
        print("Left: ", d, "cm")
        d = RightEye.read("cm", samples)
        print("Right: ", d, "cm")
        sleep(0.25)
        i += 1

    return True


report_dist()

print("Testing complete")
