#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import board
from busio import I2C
from adafruit_si7021 import SI7021


class MatildaSensorSuite(Node):
    def __init__(self):
        super().__init__("matilda_sensors")
        self.get_logger().info("Matilda Sensors Node Started")

        i2c = I2C(board.SCL, board.SDA)
        self.AtmoSensor = SI7021(i2c)

    def report_atmo():
        temperature_f = self.AtmoSensor.temperature * (9 / 5) + 32
        humidity = self.AtmoSensor.relative_humidity
        self.get_logger().info(f"The Temperature: {temperature_f:.1f} F")
        self.get_logger().info(f"The Humidity: {humidity:.1f} %")


def main(args=None):
    rclpy.init(args=args)
    node = MatildaSensorSuite()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
