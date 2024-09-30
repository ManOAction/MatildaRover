import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MatildaSensorSubscriber(Node):
    def __init__(self):
        super().__init__("matilda_sensor_subscriber")
        self.subscription = self.create_subscription(
            String, "matilda_sensors_feed", self.listener_callback, 10
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MatildaSensorSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
