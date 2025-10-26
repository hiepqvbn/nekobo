#!/usr/bin/env python3
"""Nekobo main application entrypoint.

This script initializes middleware (Arduino + controllers) and runs the main loop.
"""
import time
from middleware.bridge import Bridge
from middleware.comm.serial import SerialComm
import sys
import os
# allow running this file directly by adding repository root to sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def main():
    # Create controller manager (reads joystick or nunchuk)
    CHOSEN_CONTROLLER = "fightstick"  # "fightstick" | "nunchuk"
    if CHOSEN_CONTROLLER == "nunchuk":
        import middleware.controller.wii_nunchuk as controller_module
        controller = controller_module.WiiNunchukController()
    elif CHOSEN_CONTROLLER == "fightstick":
        import middleware.controller.hori_mini_fightstick as controller_module
        controller = controller_module.HoriMiniFightstickController()
    else:
        raise ValueError(f"Unknown controller type: {CHOSEN_CONTROLLER}")

    # Create serial comm (will attempt to auto-find port)
    # Enable verbose serial logging when NEKOBO_DEBUG env var is set.
    debug_flag = bool(os.environ.get('NEKOBO_DEBUG'))
    comm = SerialComm(verbose=debug_flag)
    comm.open()
    # start controller hardware resources
    try:
        controller.start()
    except Exception:
        pass

    bridge = Bridge(controller=controller, comm=comm)

    # In debug mode, spawn a background thread that issues heartbeat
    # requests repeatedly for a configured duration (useful for headless RP4).
    if debug_flag:
        import threading

        hb_secs = int(os.environ.get('NEKOBO_DEBUG_HEARTBEAT_SECONDS', '10'))
        hb_interval = float(os.environ.get('NEKOBO_DEBUG_HEARTBEAT_INTERVAL', '1.0'))

        def _hb_runner():
            end = time.time() + hb_secs
            while time.time() < end:
                try:
                    bridge._log('debug-heartbeat: requesting')
                    res = bridge.request_heartbeat(timeout=hb_interval)
                    if res:
                        bridge._log('debug-heartbeat: got', res)
                    else:
                        bridge._log('debug-heartbeat: no response')
                except Exception as e:
                    bridge._log('debug-heartbeat: exception', e)
                time.sleep(hb_interval)

        t = threading.Thread(target=_hb_runner, daemon=True)
        t.start()

    try:
        while True:
            feedback = bridge.run_once()
            if feedback:
                print("Feedback:", feedback)
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        comm.close()
        try:
            controller.stop()
        except Exception:
            pass


if __name__ == '__main__':
    main()
