class CommBase:
	"""Abstract base class for communication transports."""
	def open(self):
		raise NotImplementedError()

	def close(self):
		raise NotImplementedError()

	def send(self, data: str):
		raise NotImplementedError()

	def has_data(self) -> bool:
		raise NotImplementedError()

	def receive(self) -> str:
		raise NotImplementedError()
