#!/usr/bin/env python3
"""Sync protocol_setting.json -> middleware runtime protocol.json and firmware protocol.h

Usage:
  python3 software/tools/sync_protocol.py

Defaults read from:
  software/tools/protocol_setting.json

Outputs:
  software/middleware/protocol/protocol.json
  software/firmware/nekobo_v0_1_fw/protocol.h

This script is idempotent and intended to be run during development or CI to keep
middleware runtime and firmware headers in sync with the authoritative protocol
settings.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Dict, Any, List


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
SRC = TOOLS / 'protocol_setting.json'
MIDDLEWARE_PROTO_DIR = ROOT / 'middleware' / 'protocol'
MIDDLEWARE_OUT = MIDDLEWARE_PROTO_DIR / 'protocol.json'
FIRMWARE_HEADER = ROOT / 'firmware' / 'nekobo_v0_1_fw' / 'protocol.h'


def load_src(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def validate_messages(messages: Dict[str, Any]) -> None:
    ids = {}
    for name, spec in messages.items():
        if 'id' not in spec:
            raise ValueError(f"Message {name} missing 'id'")
        idtok = spec['id']
        # must be hex like 0xNN
        if not re.match(r'^0x[0-9A-Fa-f]+$', idtok):
            raise ValueError(f"Message {name} has invalid id format: {idtok}")
        if idtok in ids:
            raise ValueError(f"Duplicate id {idtok} for {name} and {ids[idtok]}")
        ids[idtok] = name


def make_middleware_messages(messages: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for name, spec in messages.items():
        args = spec.get('args', [])
        # args may be list of strings or list of objects
        arg_names: List[str] = []
        for a in args:
            if isinstance(a, dict):
                name_val = a.get('name')
                if not isinstance(name_val, str):
                    raise ValueError(f"Invalid arg def for message {name}: {a}")
                arg_names.append(name_val)
            else:
                if not isinstance(a, str):
                    raise ValueError(f"Invalid arg def for message {name}: {a}")
                arg_names.append(a)
        out[name] = {
            'id': spec['id'],
            'args': arg_names,
            'direction': spec.get('direction', 'to_arduino'),
            'description': spec.get('description', '')
        }
    return out


def write_middleware(proto: Dict[str, Any], outpath: Path) -> None:
    out = {'protocol_version': proto.get('protocol_version', 1), 'messages': proto['messages'], 'ack': proto.get('ack', {})}
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open('w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


def c_macro_name(msg_name: str) -> str:
    s = re.sub(r'[^0-9A-Za-z]', '_', msg_name)
    return 'MSG_' + s.upper()


def write_firmware_header(messages: Dict[str, Any], outpath: Path) -> None:
    guard = 'NEKOBO_PROTOCOL_H'
    lines: List[str] = []
    lines.append(f'#ifndef {guard}')
    lines.append(f'#define {guard}')
    lines.append('')
    lines.append('// Generated protocol header - do not edit by hand. Run tools/sync_protocol.py')
    lines.append('')
    lines.append('// Protocol version')
    lines.append(f'#define PROTOCOL_VERSION "{messages.get("protocol_version", 1)}"')
    lines.append('')
    # message macros
    for name, spec in messages['messages'].items():
        mid = spec['id']
        # write numeric hex literal without quotes
        lines.append(f'#define {c_macro_name(name)} {mid}')
    lines.append('')
    # basic error codes
    lines.append('// Error codes')
    lines.append('#define ERR_MISSING_ARGS 0x01')
    lines.append('')
    lines.append(f'#endif // {guard}')

    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open('w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description='Sync protocol_setting.json -> runtime and firmware')
    p.add_argument('--src', default=str(SRC), help='authoritative protocol_setting.json')
    p.add_argument('--out-middleware', default=str(MIDDLEWARE_OUT), help='output middleware runtime protocol.json')
    p.add_argument('--out-firmware', default=str(FIRMWARE_HEADER), help='output firmware header protocol.h')
    args = p.parse_args(argv)

    srcp = Path(args.src)
    if not srcp.exists():
        print('Source protocol_setting.json not found:', srcp, file=sys.stderr)
        return 2

    proto = load_src(srcp)
    messages = proto.get('messages', {})
    try:
        validate_messages(messages)
    except Exception as e:
        print('Validation error:', e, file=sys.stderr)
        return 3

    # create minimal middleware runtime
    minimal = {'protocol_version': proto.get('protocol_version', 1), 'messages': make_middleware_messages(messages), 'ack': proto.get('ack', {})}
    write_middleware(minimal, Path(args.out_middleware))
    write_firmware_header({'protocol_version': proto.get('protocol_version', 1), 'messages': minimal['messages']}, Path(args.out_firmware))

    print('Wrote middleware runtime to', args.out_middleware)
    print('Wrote firmware header to', args.out_firmware)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
