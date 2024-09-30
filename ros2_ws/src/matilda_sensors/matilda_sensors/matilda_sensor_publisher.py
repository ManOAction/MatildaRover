#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import board
from busio import I2C
from adafruit_si7021 import SI7021


class MatildaSensorPublisher(Node):
    def __init__(self):
        super().__init__("matilda_sensors_publisher")

        i2c = I2C(board.SCL, board.SDA)
        self.AtmoSensor = SI7021(i2c)

        self.publisher_ = self.create_publisher(String, "matilda_sensors_feed", 10)

        timer_period = 2
        self.AtmoTimer = self.create_timer(timer_period, self.AtmoCallback)
        self.i = 0

        self.get_logger().info("Matilda Sensors Node Started")

    def AtmoCallback(self):
        temperature_f = self.AtmoSensor.temperature * (9 / 5) + 32
        humidity = self.AtmoSensor.relative_humidity
        msg = String()
        msg.data = f"Publishing... \nThe Temperature: {temperature_f:.1f} F \n The Humidity: {humidity:.1f} %"
        self.get_logger().info(msg.data)

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MatildaSensorPublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
