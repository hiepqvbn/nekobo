# Nekobo Middleware

This folder contains the RP4 middleware layer: serial transport, protocol runtime, controller helpers and the Bridge that connects controllers to the firmware.

Location
- `software/middleware/`

Purpose
- Provide a stable, testable runtime that encodes controller intents into protocol messages and sends them to the Arduino over serial. It also decodes incoming firmware messages (sensors, heartbeats) and exposes helpers for higher-level code.

Key files
- `protocol/` — encoder/decoder and the runtime `protocol.json` used by middleware.
- `comm/serial.py` — SerialComm wrapper around the serial device.
- `arduino.py` — low-level Arduino serial helper.
- `controller/` — joystick and nunchuk helpers and `ControllerManager`.
- `bridge.py` — ties the controller to the comm using the protocol.

Running & development
1. Install Python deps (from repo root):

```bash
pip3 install -r software/requirements.txt
```

2. If you edit the authoritative protocol (`software/tools/protocol_setting.json`), regenerate the runtime mapping:

```bash
python3 software/tools/sync_protocol.py
```

3. Run the middleware directly for debugging (example):

```bash
python3 -c "from middleware import arduino; print('Find port', arduino.find_arduino())"
```

Bridge usage (example snippet)

```python
from middleware.bridge import Bridge
# controller and comm should be created as appropriate
bridge = Bridge(controller, comm)
# request heartbeat
hb = bridge.request_heartbeat(timeout=1.0)
print('hb', hb)
```

Notes
- Middleware reads its runtime protocol from `software/middleware/protocol/protocol.json`.
- The authoritative protocol is `software/tools/protocol_setting.json`; run `sync_protocol.py` to regenerate the middleware runtime mapping.

Testing
- Add pytest tests under `software/middleware/tests/` and mock `ArduinoInterface` to simulate firmware responses.
