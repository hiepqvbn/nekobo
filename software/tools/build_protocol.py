#!/usr/bin/env python3
"""Tool: build_protocol (inside software)

Reads software/protocol.json and generates a Python module with convenience builders.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROTOCOL_JSON = os.path.join(ROOT, 'protocol.json')
OUT_PY = os.path.join(ROOT, 'middleware', 'protocol_map.py')

def main():
    with open(PROTOCOL_JSON, 'r') as f:
        data = json.load(f)

    msgs = data.get('messages', [])
    lines = [
        '# Auto-generated protocol map\n',
        'def build_message(name, **kwargs):\n',
        '    # Fallback runtime builder\n',
        '    from middleware.protocol import get_protocol\n',
        '    return get_protocol().build(name, **kwargs)\n',
        '\n'
    ]

    for m in msgs:
        name = m['name']
        fmt = m['format']
        params = ', '.join([f"{f['name']}" for f in m.get('fields', [])])
        lines.append(f"def {name}({params}):\n")
        if params:
            # build with format
            args = ', '.join([f"{p}={p}" for p in params.split(', ')])
            lines.append(f"    return '{fmt}'.format({args})\n\n")
        else:
            lines.append(f"    return '{fmt}'\n\n")

    os.makedirs(os.path.dirname(OUT_PY), exist_ok=True)
    with open(OUT_PY, 'w') as f:
        f.writelines(lines)
    print('Wrote', OUT_PY)


if __name__ == '__main__':
    main()
