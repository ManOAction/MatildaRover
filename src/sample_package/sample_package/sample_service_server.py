#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts


class SampleServiceNode(Node):
    def __init__(self):
        super().__init__("sample_service")
        self.server_ = self.create_service(AddTwoInts, "add_two_ints", self.callback_pong)
        self.get_logger().info("Sample Service Class Instantiated")

    def callback_pong(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(str(request.a) + " + " + str(request.b))
        return response


def main(args=None):
    rclpy.init(args=args)
    node = SampleServiceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
