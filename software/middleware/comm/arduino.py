#!/usr/bin/env python3
"""Arduino serial interface for nekobo middleware."""
import serial
import serial.tools.list_ports
import time
from typing import Optional


def find_arduino(timeout=0.1):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p.description or "ttyACM" in p.device or "ttyUSB" in p.device:
            return p.device
    return None


class ArduinoInterface:
    def __init__(self, port: Optional[str] = None, baud: int = 57600, timeout: float = 1.0):
        self.port = port or find_arduino()
        if not self.port:
            raise FileNotFoundError("Arduino serial port not found")
        self.baud = baud
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None

    def open(self):
        if self.ser and self.ser.is_open:
            return
        self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        # give Arduino a moment
        time.sleep(0.1)

    def close(self):
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass

    def send(self, cmd: str):
        if not self.ser or not self.ser.is_open:
            self.open()
        assert self.ser is not None
        if not cmd.endswith("\n"):
            cmd = cmd + "\n"
        self.ser.write(cmd.encode("utf-8"))

    def readline(self) -> str:
        if not self.ser or not self.ser.is_open:
            self.open()
        assert self.ser is not None
        return self.ser.readline().decode(errors="ignore").strip()
