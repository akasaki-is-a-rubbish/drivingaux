from serial import Serial

s = Serial("/dev/ttyUSB0", baudrate=115200, timeout=10)

