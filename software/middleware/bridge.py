"""Bridge: connect controller -> comm with protocol encoding."""

from .protocol import encoder, decoder


class Bridge:
    def __init__(self, controller, comm):
        self.controller = controller
        self.comm = comm
        # encoder/decoder are provided by the middleware.protocol package
        self.last_heartbeat = None
        self.last_heartbeat_time = None
        # Bridge-level verbosity: prefer comm._log when available
        self._verbose = getattr(comm, 'verbose', False)

    def _log(self, *args, **kwargs):
        """Simple logging helper that leverages comm._log when present."""
        if hasattr(self.comm, '_log') and callable(getattr(self.comm, '_log')):
            try:
                # forward to comm logger for consistent prefixing
                self.comm._log(*args, **kwargs)
                return
            except Exception:
                pass
        if not self._verbose:
            return
        import time
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        print('[Bridge]', ts, *args, **kwargs)

    def run_once(self):
        """Perform a single read-encode-send cycle and process one incoming line if present."""
        self._log('run_once: polling controller')
        try:
            input_data = self.controller.read_input()
        except Exception as e:
            self._log('run_once: controller.read_input() raised', e)
            input_data = None

        if not input_data:
            self._log('run_once: no input')
            return
        self._log('run_once: got input', input_data)
        t = input_data.get('type')
        if t == 'MOVE':
            msg = encoder.encode('MOVE', speed_left=input_data['speed_left'], speed_right=input_data['speed_right'])
            self._log('run_once: encoded MOVE ->', msg)
            self.comm.send(msg)
        elif t == 'STOP':
            msg = encoder.encode('STOP')
            self._log('run_once: encoded STOP ->', msg)
            self.comm.send(msg)

        # try to receive one line
        try:
            raw = self.comm.receive()
            if not raw:
                self._log('run_once: no incoming data')
                return None
            self._log('run_once: raw incoming ->', raw)
            decoded = decoder.decode(raw)
            self._log('run_once: decoded ->', decoded)
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
        except Exception as e:
            self._log('run_once: exception while receiving/decoding', e)
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
        self._log('request_heartbeat: sending', msg)
        self.comm.send(msg)

        # wait for response until timeout
        import time
        end = time.time() + timeout
        while time.time() < end:
            try:
                raw = self.comm.receive()
            except Exception:
                self._log('request_heartbeat: receive() raised')
                return None
            if not raw:
                self._log('request_heartbeat: no data yet')
                continue
            decoded = decoder.decode(raw)
            self._log('request_heartbeat: decoded ->', decoded)
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

