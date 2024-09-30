from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    node1 = Node(
        package='matilda_sensors',
        executable='sensor_publisher',
        name='sensor_publisher',
        output='screen'
    )

    node2 = Node(
        package='matilda_sensors',
        executable='matilda_sensor_server',
        name='matilda_sensor_server',
        output='screen'
    )

    return LaunchDescription([node1])