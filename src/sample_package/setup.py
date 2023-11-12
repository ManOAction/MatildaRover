from setuptools import find_packages, setup

package_name = "sample_package"

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
            "sample_node = sample_package.sample_node:main",
            "sample_node2 = sample_package.sample_node2:main",
            "sample_service_server = sample_package.sample_service_server:main",
            "sample_service_client = sample_package.sample_service_client:main",
        ]
    },
)
