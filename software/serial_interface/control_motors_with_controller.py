import pygame
import serial
import time

# Connect serial to Arduino
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    pygame.event.pump()
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Map axis to motor command
    left_speed = int(100 * (y_axis - x_axis))
    right_speed = int(100 * (y_axis + x_axis))

    cmd = f"{left_speed},{right_speed}\n"
    ser.write(cmd.encode('utf-8'))

    print("Sent:", cmd)
    time.sleep(0.1)
