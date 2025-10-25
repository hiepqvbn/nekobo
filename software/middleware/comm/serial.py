from .base import CommBase
from .arduino import ArduinoInterface
from typing import Optional
import time


class SerialComm(CommBase):
	"""Serial communication wrapper with optional verbose debug prints.

	When `verbose` is True the class prints connection steps and every
	outbound/inbound line to stdout with a small timestamp prefix. This
	helps debugging headless runs on the Pi where no GUI is available.
	"""

	def __init__(self, port: Optional[str] = None, baud: int = 57600, timeout: float = 0.1, verbose: bool = False):
		self.port = port
		self.baud = baud
		self.timeout = timeout
		self.arduino: Optional[ArduinoInterface] = None
		self.verbose = verbose

	def _log(self, *args, **kwargs):
		if not self.verbose:
			return
		ts = time.strftime('%Y-%m-%d %H:%M:%S')
		print('[SerialComm]', ts, *args, **kwargs)

	def open(self):
		self._log('Opening serial comm', {'port': self.port, 'baud': self.baud, 'timeout': self.timeout})
		try:
			self.arduino = ArduinoInterface(port=self.port, baud=self.baud, timeout=self.timeout)
			self.arduino.open()
			self._log('Serial port opened', getattr(self.arduino, 'port', self.port))
		except Exception as e:
			# Don't swallow - rethrow after logging so callers can handle
			self._log('Failed to open serial port:', e)
			raise

	def close(self):
		self._log('Closing serial comm')
		if self.arduino:
			try:
				self.arduino.close()
				self._log('Serial port closed')
			except Exception as e:
				self._log('Error closing serial port:', e)

	def send(self, data: str):
		"""Send a line to the Arduino. Prints the outgoing command when verbose."""
		if not self.arduino:
			try:
				self.open()
			except Exception:
				# open() already logged the failure
				return
		assert self.arduino is not None
		out = data.strip() if data is not None else ''
		self._log('SEND ->', out)
		try:
			self.arduino.send(data)
		except Exception as e:
			self._log('Error sending data:', e)

	def has_data(self) -> bool:
		# Keep the original conservative behavior; rely on receive() timeout
		return False

	def receive(self) -> str:
		"""Read one line from the Arduino and print it when verbose.

		Returns an empty string when nothing was received within timeout.
		"""
		if not self.arduino:
			try:
				self.open()
			except Exception:
				return ''
		assert self.arduino is not None
		try:
			raw = self.arduino.readline()
		except Exception as e:
			self._log('Error reading from serial:', e)
			return ''
		if raw:
			self._log('RECV <-', raw)
		return raw
