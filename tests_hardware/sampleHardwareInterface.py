import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Float64


class RoverHardwareInterface(Node):
    def __init__(self):
        super().__init__("rover_hardware_interface")

        # Initialize motors and sensors
        self.left_wheel_cmd = 0.0
        self.right_wheel_cmd = 0.0
        self.left_wheel_position = 0.0
        self.left_wheel_velocity = 0.0
        self.right_wheel_position = 0.0
        self.right_wheel_velocity = 0.0

        # ROS2 Publishers for wheel commands
        self.left_wheel_cmd_pub = self.create_publisher(
            Float64, "/left_wheel_velocity_cmd", QoSProfile(depth=10)
        )
        self.right_wheel_cmd_pub = self.create_publisher(
            Float64, "/right_wheel_velocity_cmd", QoSProfile(depth=10)
        )

        # ROS2 Subscribers for wheel state
        self.left_wheel_position_sub = self.create_subscription(
            Float64, "/left_wheel_position", self.left_wheel_position_callback, QoSProfile(depth=10)
        )
        self.left_wheel_velocity_sub = self.create_subscription(
            Float64, "/left_wheel_velocity", self.left_wheel_velocity_callback, QoSProfile(depth=10)
        )
        self.right_wheel_position_sub = self.create_subscription(
            Float64,
            "/right_wheel_position",
            self.right_wheel_position_callback,
            QoSProfile(depth=10),
        )
        self.right_wheel_velocity_sub = self.create_subscription(
            Float64,
            "/right_wheel_velocity",
            self.right_wheel_velocity_callback,
            QoSProfile(depth=10),
        )

    def left_wheel_position_callback(self, msg):
        self.left_wheel_position = msg.data

    def left_wheel_velocity_callback(self, msg):
        self.left_wheel_velocity = msg.data

    def right_wheel_position_callback(self, msg):
        self.right_wheel_position = msg.data

    def right_wheel_velocity_callback(self, msg):
        self.right_wheel_velocity = msg.data

    def publish_wheel_commands(self):
        left_wheel_msg = Float64()
        left_wheel_msg.data = self.left_wheel_cmd
        right_wheel_msg = Float64()
        right_wheel_msg.data = self.right_wheel_cmd

        self.left_wheel_cmd_pub.publish(left_wheel_msg)
        self.right_wheel_cmd_pub.publish(right_wheel_msg)


def main(args=None):
    rclpy.init(args=args)

    rover_hw_interface = RoverHardwareInterface()

    while rclpy.ok():
        rover_hw_interface.publish_wheel_commands()
        rclpy.spin_once(rover_hw_interface)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
