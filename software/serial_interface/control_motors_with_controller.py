import pygame
import serial
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Controller:", joystick.get_name())
print(f"Detected {joystick.get_numaxes()} axes")

def send_command(left, right):
    cmd = f"{left},{right}\n"
    ser.write(cmd.encode('utf-8'))
    print(f"Sent: {cmd.strip()}")

try:
    while True:
        pygame.event.pump()
        x = joystick.get_axis(6)  # Hat0X
        y = joystick.get_axis(7)  # Hat0Y

        # Convert from [-32767, 0, 32767] to -1, 0, 1
        x = int(x / 32767) if x != 0 else 0
        y = int(y / 32767) if y != 0 else 0

        # Movement logic
        if y == -1 and x == 0:
            send_command(100, 100)  # Forward
        elif y == 1 and x == 0:
            send_command(-100, -100)  # Backward
        elif y == 0 and x == -1:
            send_command(-100, 100)  # Turn left
        elif y == 0 and x == 1:
            send_command(100, -100)  # Turn right
        elif y == -1 and x == -1:
            send_command(50, 100)  # Forward-left
        elif y == -1 and x == 1:
            send_command(100, 50)  # Forward-right
        elif y == 1 and x == -1:
            send_command(-50, -100)  # Backward-left
        elif y == 1 and x == 1:
            send_command(-100, -50)  # Backward-right
        else:
            send_command(0, 0)  # Stop

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()
    pygame.quit()
