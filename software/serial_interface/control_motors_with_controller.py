import pygame
import serial
import time

# === CONFIG ===
SERIAL_PORT = '/dev/ttyACM0'  # check with ls /dev/ttyACM*
BAUD_RATE = 115200

# === INIT SERIAL ===
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# === INIT PYGAME JOYSTICK ===
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Controller:", joystick.get_name())
print("Ready. Press Ctrl+C to stop.")


def map_axis(val):
    # Map from -32767~32767 → -100~100
    return int(val / 32767 * 100)


try:
    while True:
        pygame.event.pump()
        x = map_axis(joystick.get_axis(6))  # Left(-) / Right(+)
        y = map_axis(joystick.get_axis(7))  # Up(-) / Down(+)

        # Compute motor speed (simple differential drive)
        left_speed = y - x
        right_speed = y + x

        # Limit to -100~100
        left_speed = max(-100, min(100, left_speed))
        right_speed = max(-100, min(100, right_speed))

        cmd = f"{left_speed},{right_speed}\n"
        ser.write(cmd.encode('utf-8'))

        print(f"Sent: {cmd.strip()}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()
    pygame.quit()
