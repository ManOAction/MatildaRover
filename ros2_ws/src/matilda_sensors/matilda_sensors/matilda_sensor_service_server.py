#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from matilda_interfaces.srv import SensorMeasurement

import board
from busio import I2C

from adafruit_fxos8700 import FXOS8700  # accelo / magnetometer
from adafruit_fxas21002c import FXAS21002C  # gyro
from adafruit_si7021 import SI7021  # temp and humidiy
from gpiozero import LED, Motor
from time import sleep

i2c = I2C(board.SCL, board.SDA)
AtmoSensor = SI7021(i2c)
Magnetometer = FXOS8700(i2c)
Gyro_Accel = FXAS21002C(i2c)
MotorSpeed = float(".3")
RMotor = Motor(13, 6)
LMotor = Motor(19, 26)


class MatildaSensorServiceNode(Node):
    def __init__(self):
        super().__init__("matilda_sensor_service")
        self.server_ = self.create_service(
            SensorMeasurement, "matilda_sensor_service", self.callback_sensor_read
        )
        self.get_logger().info("Matilda Sensor Service Started")

    def callback_sensor_read(self, request, response):
        if request.sensor == "Si7021":
            response.sensor_response = self.Si7021Reading()
            return response

        if request.sensor == "9-DOF":
            response.sensor_response = self.NineDOFReading()
            return response

        if request.sensor == "MotorTest":
            response.sensor_response = self.MotorTest()
            return response

        else:
            msg = f"Unkown Sensor Request"
            self.get_logger().info(msg)
            response.sensor_response = msg
            return response

    def Si7021Reading(self):
        self.get_logger().info("Responding to Si7021 Request")
        temperature_f = AtmoSensor.temperature * (9 / 5) + 32
        humidity = AtmoSensor.relative_humidity

        msg = f"The Temperature: {temperature_f:.1f} F and The Humidity: {humidity:.1f} %"
        self.get_logger().info(msg)

        return msg

    def NineDOFReading(self):
        self.get_logger().info("Responding to fxos8700 and fxas21002c 9-DOF Request")

        mag_x, mag_y, mag_z = Magnetometer.magnetometer
        gyro_x, gyro_y, gyro_z = Gyro_Accel.gyroscope

        msg = f"""
        Results of magnetometer call: {mag_x}, {mag_y}, {mag_z}
        Results of gyroscope call: {gyro_x}, {gyro_y}, {gyro_z}
        """
        self.get_logger().info(msg)

        return msg

    def MotorTest(self):
        self.get_logger().info("Responding to request for motor test.")

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

        msg = "Testing complete"

        return msg


def main(args=None):
    rclpy.init(args=args)
    node = MatildaSensorServiceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
