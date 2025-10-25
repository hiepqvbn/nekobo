"""Bridge: connect controller -> comm with protocol encoding."""

from .protocol import encoder, decoder


class Bridge:
    def __init__(self, controller, comm):
        self.controller = controller
        self.comm = comm
        # encoder/decoder are provided by the middleware.protocol package
        self.last_heartbeat = None
        self.last_heartbeat_time = None

    def run_once(self):
        """Perform a single read-encode-send cycle and process one incoming line if present."""
        input_data = self.controller.read_input()
        if not input_data:
            return
        t = input_data.get('type')
        if t == 'MOVE':
            msg = encoder.encode('MOVE', speed_left=input_data['speed_left'], speed_right=input_data['speed_right'])
            self.comm.send(msg)
        elif t == 'STOP':
            msg = encoder.encode('STOP')
            self.comm.send(msg)

        # try to receive one line
        try:
            raw = self.comm.receive()
            if raw:
                decoded = decoder.decode(raw)
                # if heartbeat response, store it
                if decoded and decoded.get('name') == 'HEARTBEAT_RESP':
                    # store parsed values
                    self.last_heartbeat = {
                        'init_ms': decoded.get('init_ms'),
                        'loop_ms': decoded.get('loop_ms'),
                        'raw': raw.strip()
                    }
                    import time as _time
                    self.last_heartbeat_time = _time.time()
                return decoded
        except Exception:
            return None

    def request_heartbeat(self, timeout: float = 1.0):
        """Send HEARTBEAT_REQ and wait (blocking) up to timeout seconds for a HEARTBEAT_RESP.

        Returns the heartbeat dict on success, or None on timeout/error.
        """
        # send request
        try:
            msg = encoder.encode('HEARTBEAT_REQ')
        except KeyError:
            # protocol does not support heartbeat
            return None
        self.comm.send(msg)

        # wait for response until timeout
        import time
        end = time.time() + timeout
        while time.time() < end:
            try:
                raw = self.comm.receive()
            except Exception:
                return None
            if not raw:
                continue
            decoded = decoder.decode(raw)
            if decoded and decoded.get('name') == 'HEARTBEAT_RESP':
                self.last_heartbeat = {
                    'init_ms': decoded.get('init_ms'),
                    'loop_ms': decoded.get('loop_ms'),
                    'raw': raw.strip()
                }
                self.last_heartbeat_time = time.time()
                return self.last_heartbeat
        return None

    def get_last_heartbeat(self):
        """Return last heartbeat dict or None."""
        return self.last_heartbeat

