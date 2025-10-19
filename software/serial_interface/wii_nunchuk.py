#!/usr/bin/env python3
import smbus2
import time

# === I2C setup for Nunchuck ===
address = 0x52

def init_nunchuck(bus):
    bus.write_byte_data(address, 0x40, 0x00)
    time.sleep(0.1)

# def read_nunchuck(bus):
#     try:
#         bus.write_byte(address, 0x00)
#         time.sleep(0.002)
#         data = bus.read_i2c_block_data(address, 0, 6)
#         return data
#     except OSError:
#         print("Warning: I2C communication lost - reinitializing...")
#         time.sleep(0.1)
#         init_nunchuck(bus)
#         return None

# Initialize Nunchuck
bus = smbus2.SMBus(1)
init_nunchuck(bus)

def read_nunchuck():
    try:
        bus.write_byte(address, 0x00)
        time.sleep(0.002)
        data = [bus.read_byte(address) for _ in range(6)]
        data = [(x ^ 0x17) + 0x17 for x in data]  # decode
        return data
    except OSError:
        print("Warning: I2C communication lost - reinitializing...")
        time.sleep(0.1)
        init_nunchuck(bus)
        return None

def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# === Control Loop ===
print("Ready to drive with Nunchuck")

while True:
    try:
        data = read_nunchuck()
        if data:
            # joy_x, joy_y, accel_x, accel_y, accel_z, buttons = data
            joy_x, joy_y,accel_x,accel_y,accel_z, z_btn, c_btn = data[0], data[1],data[2],data[3], data[4], data[5] & 0x01, (data[5] >> 1) & 0x01
            # print(f'{joy_x=}; {joy_y=}; {accel_x=}; {accel_y=}; {accel_z=}; {buttons=}')
            print(f'{joy_x=}; {joy_y=}; {accel_x=}; {accel_y=}; {accel_z=}; {z_btn=}; {c_btn=}')

            # center joystick is around (128,128)
            x_offset = joy_x - 128
            y_offset = joy_y - 128

        time.sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting...")
        break
