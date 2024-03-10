from setuptools import find_packages, setup

package_name = "matilda_sensors"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jacob",
    maintainer_email="jacobleis@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "sensor_publisher = matilda_sensors.matilda_sensor_publisher:main",
            "sensor_subscriber = matilda_sensors.matilda_sensor_subscriber:main",
            "matilda_sensor_server = matilda_sensors.matilda_sensor_service_server:main",
            "matilda_sensor_client = matilda_sensors.matilda_sensor_service_client:main",
            "subscriber_test = matilda_sensors.subscriber_test_function:main",
            "publisher_test = matilda_sensors.publisher_test_function:main",
        ],
    },
)
