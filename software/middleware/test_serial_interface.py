import serial
import time

# For USB connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # wait for Arduino reset

print("Type command (forward X / backward X / stop):")
while True:
    cmd = input("> ").strip()
    if cmd == "exit":
        break
    ser.write((cmd + "\n").encode())
    feedback = ser.readline().decode().strip()
    if feedback:
        print("Arduino:", feedback)
