# Nekobo Application

This folder contains the high-level application entrypoint for Nekobo.

Location
- `software/application/`

Purpose
- Provide a single entrypoint (`nekobo_main.py`) that composes the ControllerManager, SerialComm and Bridge to run the robot.

Running
- From the repo root (recommended):

```bash
python3 -m application.nekobo_main
```

- Or use the startup script (on RP4):

```bash
software/tools/startup/run_nekobo.sh
```

Monitoring & heartbeat
- The Bridge exposes a `request_heartbeat()` helper. You can periodically call it to assert firmware health. Example:

```python
hb = bridge.request_heartbeat(timeout=1.0)
if hb:
    print('Arduino init_ms', hb['init_ms'], 'loop_ms', hb['loop_ms'])
else:
    print('No heartbeat')
```

Logs
- When run via systemd, view logs with:

```bash
sudo journalctl -u nekobo.service -f
```

Notes
- Ensure `PYTHONPATH` includes the repo root so imports resolve when using the startup script (the provided `run_nekobo.sh` sets this up).
