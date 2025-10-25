from .base import CommBase
from ..arduino import ArduinoInterface
from typing import Optional
import time


class SerialComm(CommBase):
	def __init__(self, port: Optional[str] = None, baud: int = 57600, timeout: float = 0.1):
		self.port = port
		self.baud = baud
		self.timeout = timeout
		self.arduino: Optional[ArduinoInterface] = None

	def open(self):
		self.arduino = ArduinoInterface(port=self.port, baud=self.baud, timeout=self.timeout)
		self.arduino.open()

	def close(self):
		if self.arduino:
			self.arduino.close()

	def send(self, data: str):
		if not self.arduino:
			self.open()
		assert self.arduino is not None
		self.arduino.send(data)

	def has_data(self) -> bool:
		# Not a perfect check; rely on readline with small timeout instead
		return False

	def receive(self) -> str:
		if not self.arduino:
			self.open()
		assert self.arduino is not None
		return self.arduino.readline()
