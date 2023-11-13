#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from matilda_interfaces.srv import SensorMeasurement

import board
from busio import I2C
from adafruit_si7021 import SI7021

i2c = I2C(board.SCL, board.SDA)
AtmoSensor = SI7021(i2c)


class MatildaSensorServiceNode(Node):
    def __init__(self):
        super().__init__("matilda_sensor_service")
        self.server_ = self.create_service(
            SensorMeasurement, "matilda_sensor_service", self.callback_sensor_read
        )
        self.get_logger().info("Matilda Sensor Service Started")

    def callback_sensor_read(self, request, response):
        if request.sensor == "Si7021":
            response = self.Si7021Reading()

        else:
            response = "Unknown Sensor Request"

        return response

    def Si7021Reading(self):
        self.get_logger().info("Responding to Si7021 Request")
        temperature_f = AtmoSensor.temperature * (9 / 5) + 32
        humidity = AtmoSensor.relative_humidity

        msg = f"The Temperature: {temperature_f:.1f} F \n The Humidity: {humidity:.1f} %"
        self.get_logger().info(msg)

        return msg


def main(args=None):
    rclpy.init(args=args)
    node = MatildaSensorServiceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
