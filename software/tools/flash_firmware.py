#!/usr/bin/env python3
"""Tool: flash_firmware (inside software)

Attempts to compile & flash the Arduino firmware using `arduino-cli`.
If `arduino-cli` is not installed, prints instructions.
"""
import shutil
import subprocess
import os
import sys

SKETCH_DIR = os.path.join(os.path.dirname(__file__), '..', 'firmware', 'nekobo_v0_1_fw')

def main():
    if shutil.which('arduino-cli') is None:
        print('arduino-cli not found. Install it: https://arduino.github.io/arduino-cli/latest/installation/')
        print('Or upload the sketch in', SKETCH_DIR, 'with the Arduino IDE')
        return

    fqbn = 'arduino:avr:uno'  # adjust to your board
    cmd_compile = ['arduino-cli', 'compile', '--fqbn', fqbn, SKETCH_DIR]
    print('Compiling...')
    subprocess.check_call(cmd_compile)

    # find port
    print('Please connect the board and set the serial port (e.g. /dev/ttyACM0).')
    port = input('Serial port (or leave empty to skip upload): ').strip()
    if not port:
        print('Upload skipped')
        return

    cmd_upload = ['arduino-cli', 'upload', '-p', port, '--fqbn', fqbn, SKETCH_DIR]
    print('Uploading...')
    subprocess.check_call(cmd_upload)
    print('Done')


if __name__ == '__main__':
    main()
