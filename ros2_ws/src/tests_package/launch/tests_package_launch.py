from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    node1 = Node(
        package='tests_package',
        executable='pub_test',
        name='publisher_test',
        output='screen'
    )

    return LaunchDescription([node1])