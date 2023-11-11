#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class SampleServiceNode(Node):  # MODIFY NAME
    def __init__(self):
        super().__init__("sample_service")  # MODIFY NAME
        self.get_logger().info("Sample Service Class Instantiated")


def main(args=None):
    rclpy.init(args=args)
    node = SampleServiceNode()  # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
