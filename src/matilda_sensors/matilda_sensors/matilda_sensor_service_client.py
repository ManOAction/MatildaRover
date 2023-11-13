#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from matilda_interfaces.srv import SensorMeasurement


MenuOptions = """
#############
Matilda Sensor Service Client Menu

t for Temperature Reading
o for 9-DOF Reading
b for a Bad Request

q to quit the interface

#############
"""
MenuTranslation = {"t": "Si7021", "o": "9-DOF", "b": "BadRequest"}


class MatildaSensorServiceClient(Node):
    def __init__(self):
        super().__init__("matilda_sensor_service_client")
        self.get_logger().info("Matilda Sensor Service Client started.")

    def call_sensor_service(self, sensor):
        # Creating the service client
        client = self.create_client(SensorMeasurement, "matilda_sensor_service")

        # Waiting for the service to be available
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service matilda_sensor_service")

        # Creating the request instance from the srv file
        request = SensorMeasurement.Request()
        request.sensor = sensor  # Setting the request instance with the sensor name


        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        try:
            response = future.result()
            print("Server Responded:")
            print(f"{response.sensor_response}")
            input("Press Enter to Return to Menu: ")

        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    MatildaSensorClient = MatildaSensorServiceClient()

    while True:
        print(MenuOptions)
        selection = input("Select a sensor: ")

        if selection == 'q':
            break

        if selection in MenuTranslation:
            print(f"\n \nMaking call to Sensor: {MenuTranslation[selection]}")
            MatildaSensorClient.call_sensor_service(MenuTranslation[selection])

        else:
            print("Invalid Selection")

    rclpy.shutdown()


if __name__ == "__main__":
    main()
