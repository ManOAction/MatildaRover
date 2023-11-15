import serial.tools.list_ports
import serial
import time
import toml

# Read config file
with open("config.toml", "r") as f:
    Config = toml.load(f)


def find_arduino_port():
    arduino_vendor_id = Config["BoardInfo"]["VID"]
    arduino_product_id = Config["BoardInfo"]["PID"]

    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(port)
        print(port.vid)
        print(port.pid)
        print(port.name)
        print(port.manufacturer)
        print(port.product)
        if port.vid == int(arduino_vendor_id, 16) and port.pid == int(arduino_product_id, 16):
            return port.device

    return None


arduino_port = find_arduino_port()

if arduino_port is not None:
    print(f"Arduino found on {arduino_port}")
    ser = serial.Serial(arduino_port, 9600)

    # Your communication logic here

    ser.close()
else:
    print("Arduino not found.")
