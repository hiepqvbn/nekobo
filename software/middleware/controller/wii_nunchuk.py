#!/usr/bin/env python3
"""Module to interact with a Wii Nunchuk over I2C.

This file provides a BaseController implementation that initializes the
Nunchuk bus and converts raw readings into high-level MOVE/STOP commands.
It is import-safe (won't hard-fail if smbus2 is missing) and tries to be
robust on read errors.
"""
from typing import Optional, Dict, Any
import time
try:
    import smbus2
except Exception:
    smbus2 = None

from .base import BaseController

# === I2C setup for Nunchuck ===
address = 0x52


class WiiNunchukController(BaseController):
    def __init__(self, name: str = "wii_nunchuk", bus_number: int = 1) -> None:
        super().__init__(name=name)
        self.bus_number = bus_number
        self.bus = None

    def start(self) -> None:
        if smbus2 is None:
            self.bus = None
            return
        try:
            self.bus = smbus2.SMBus(self.bus_number)
            # initialize
            self.bus.write_byte_data(address, 0x40, 0x00)
            time.sleep(0.05)
        except Exception:
            self.bus = None
        super().start()

    def stop(self) -> None:
        try:
            if self.bus:
                self.bus.close()
        except Exception:
            pass
        self.bus = None
        super().stop()

    def read_input(self) -> Optional[Dict[str, Any]]:
        """Read nunchuk and convert to MOVE/STOP or None.

        Returns None on transient read errors or if the bus is unavailable.
        """
        if not self.bus:
            return None
        try:
            # Request 6 bytes
            self.bus.write_byte(address, 0x00)
            time.sleep(0.002)
            raw = [self.bus.read_byte(address) for _ in range(6)]
            data = [(x ^ 0x17) + 0x17 for x in raw]
            # decode axes
            joystick_x = data[0]
            joystick_y = data[1]
            # map joystick (0..255) to -1..1 centered at ~128
            cx = (joystick_x - 128) / 128.0
            cy = (joystick_y - 128) / 128.0
            # deadzone
            if abs(cx) < 0.15 and abs(cy) < 0.15:
                return {"type": "STOP"}
            # map to speeds
            forward = int(max(-1.0, min(1.0, -cy)) * 200)
            turn = int(max(-1.0, min(1.0, cx)) * 100)
            left = forward + turn
            right = forward - turn
            return {"type": "MOVE", "speed_left": int(left), "speed_right": int(right)}
        except OSError:
            # transient I2C issue; caller may retry later
            return None


def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == '__main__':
    # Run visual test harness in base using this controller instance.
    import importlib.util
    import os

    base_path = os.path.join(os.path.dirname(__file__), 'base.py')
    spec = importlib.util.spec_from_file_location('controller_base', base_path)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)

    c = WiiNunchukController()
    base.run_visual_test(c)

