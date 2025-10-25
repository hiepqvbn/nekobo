Nekobo (software) — 3-layer robot architecture (firmware -> middleware -> application)

This directory contains the full software stack:

- firmware: Arduino sketch (software/firmware/nekobo_v0_1_fw)
- middleware: Python helpers for serial, controller, and protocol (software/middleware)
- application: runner (software/application/nekobo_main.py)
- tools/: CLI helpers to build protocol mapping and flash firmware

Quickstart (from the repo root):

1. Install Python deps:

```bash
pip3 install -r software/requirements.txt
```

2. Generate protocol map (optional):

```bash
python3 software/tools/build_protocol.py
```

3. Run the application (from repo root):

```bash
python3 software/application/nekobo_main.py
```

4. To flash firmware with `arduino-cli`:

```bash
python3 software/tools/flash_firmware.py
```

---

## Startup on Raspberry Pi (RP4)

Follow these steps to install and run Nekobo as a system service on an RP4.

1) Copy repository to RP4 (for example `/home/pi/nekobo`).

2) (Optional) Create a virtualenv and install dependencies:

```bash
cd /home/pi/nekobo/software
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

3) Copy the systemd template and edit paths if needed (the template is now in `software/tools/startup/`):

```bash
sudo cp software/tools/startup/nekobo.service.template /etc/systemd/system/nekobo.service
# edit /etc/systemd/system/nekobo.service to set User, WorkingDirectory and ExecStart if necessary
sudo systemctl daemon-reload
sudo systemctl enable nekobo.service
sudo systemctl start nekobo.service
sudo journalctl -u nekobo.service -f
```

4) Debugging
- Logs: `sudo journalctl -u nekobo.service -f`
- Run manually: `/home/pi/nekobo/software/tools/startup/run_nekobo.sh`

## Generating protocol artifacts (sync)

When you change the canonical protocol settings, run the sync tool to generate
the runtime mapping for the RP4 middleware and the firmware protocol header.

From the repository root run:

```bash
python3 software/tools/sync_protocol.py
```

This reads `software/tools/protocol_setting.json` and writes:
- `software/middleware/protocol/protocol.json` (minimal runtime mapping used by middleware)
- `software/firmware/nekobo_v0_1_fw/protocol.h` (C macros used by the firmware)

If you want to customize paths, the script supports `--src`, `--out-middleware`, and
`--out-firmware` options.

