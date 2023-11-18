import serial.tools.list_ports
import toml
import serial
import time
from icecream import ic

# Read config file
with open("config.toml", "r") as f:
    Config = toml.load(f)


def find_arduino_port():
    arduino_vendor_id = Config["BoardInfo"]["VID"]
    arduino_product_id = Config["BoardInfo"]["PID"]

    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if port.vid == int(arduino_vendor_id, 16) and port.pid == int(arduino_product_id, 16):
            return port.device

    return None


arduino_port = find_arduino_port()

if arduino_port is not None:
    ic(f"Arduino found on {arduino_port}")

else:
    ic("Arduino not found.")
    exit(1)

# Define the serial port and baud rate

ic("Opening serial port...")
ser = serial.Serial(arduino_port, 9600, timeout=5)

# Allow some time for the Arduino to initialize
ic("Waiting for Arduino to initialize...")
time.sleep(3)

# Send data to Arduino
ic("Sending data to Arduino...")
ser.write(b"Hello, Arduino!")

# Wait for a moment
ic("Waiting for Arduino to respond...")
time.sleep(1)

# Read data from Arduino
ic("Reading data from Arduino...")
response = ser.readline().decode("utf-8").strip()
print(f"Arduino says: {response}")

# Close the serial connection
ser.close()
