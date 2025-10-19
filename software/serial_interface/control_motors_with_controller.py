import pygame
import serial
import time
import serial.tools.list_ports


def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # Look for Arduino-like devices
        if "Arduino" in p.description or "ttyACM" in p.device or "ttyUSB" in p.device:
            print(f"Found Arduino on port: {p.device}")
            return p.device
    raise Exception("Arduino not found. Check USB connection.")


# Use it
try:
    SERIAL_PORT = find_arduino()
    BAUD_RATE = 115200
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino at {SERIAL_PORT}")
except Exception as e:
    print(e)

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Controller:", joystick.get_name())
print(f"Detected {joystick.get_numhats()} hats.")

direction_map = {
    "forward": "dir 0 -1",
    "backward": "dir 0 1",
    "left": "dir -1 0",
    "right": "dir 1 0",
    "forward-left": "dir -1 -1",
    "forward-right": "dir 1 -1",
    "backward-left": "dir -1 1",
    "backward-right": "dir 1 1",
    "stop": "dir 0 0"
}


def set_direction(x, y):
    if y == 1 and x == 0:
        return "forward"
    elif y == -1 and x == 0:
        return "backward"
    elif y == 0 and x == -1:
        return "left"
    elif y == 0 and x == 1:
        return "right"
    elif y == 1 and x == -1:
        return "forward-left"
    elif y == 1 and x == 1:
        return "forward-right"
    elif y == 1 and x == -1:
        return "backward-left"
    elif y == -1 and x == 1:
        return "backward-right"
    else:
        return "stop"


def send_command(cmd):
    cmd = f"{cmd}\n"
    ser.write(cmd.encode('utf-8'))
    print(f"Sent: {cmd.strip()}")


try:
    while True:
        pygame.event.pump()
        hat = joystick.get_hat(0)  # Hat0X

        x = hat[0]
        y = hat[1]

        # Movement logic
        direction = set_direction(x, y)
        command = direction_map[direction]
        send_command(command)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()
    pygame.quit()
