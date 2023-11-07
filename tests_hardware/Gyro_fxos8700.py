import board
from busio import I2C
from adafruit_fxos8700 import FXOS8700  # accelo / magnetometer
from adafruit_fxas21002c import FXAS21002C  # gyro


i2c = I2C(board.SCL, board.SDA)

# Initializing Gyro and Magnetometer
Magnetometer = FXOS8700(i2c)
Gyro_Accel = FXAS21002C(i2c)

mag_x, mag_y, mag_z = Magnetometer.magnetometer

print(f"Results of magnetometer call: {mag_x}, {mag_y}, {mag_z}")

gyro_x, gyro_y, gyro_z = Gyro_Accel.gyroscope

print(f"Results of gyroscope call: {gyro_x}, {gyro_y}, {gyro_z}")

print("Testing complete")
