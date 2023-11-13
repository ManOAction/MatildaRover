#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from matilda_interfaces.srv import SensorMeasurement


MenuOptions = """
    #############
    Matilda Sensor Service Client Menu

    t for Temperature Reading
    b for a Bad Request

    #############
"""
MenuTranslation = {"t": "Si7021", "b": "BadRequest"}


class MatildaSensorServiceClient(Node):
    def __init__(self):
        super().__init__("matilda_sensor_service_client")
        self.get_logger().info("Matilda Sensor Service Client started.")
        self.sensor_menu()

    def sensor_menu(self):
        print(MenuOptions)
        selection = input("Select a sensor: ")

        if selection in MenuTranslation:
            print(f"Making call to Sensor: {MenuTranslation[selection]}")
            self.call_sensor_service(MenuTranslation[selection])

        else:
            print("Invalid Selection")

    def call_sensor_service(self, sensor):
        # Creating the service client
        client = self.create_client(SensorMeasurement, "matilda_sensor_service")

        # Waiting for the service to be available
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service matilda_sensor_service")

        # Creating the request instance from the srv file
        request = SensorMeasurement.Request()
        request.sensor = sensor  # Setting the request instance with the sensor name

        print("Request Package Info:")
        print(request)
        print(request.sensor)

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call_sensor_service, sensor=sensor))

    def callback_call_sensor_service(self, future, sensor):
        print("Inside Callback Loop")
        print(future)
        print(sensor)
        print(future.result())
        try:
            response = future.result()
            print("Server Responded:")
            print(f"{response.sensor_response}")

        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = MatildaSensorServiceClient()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
