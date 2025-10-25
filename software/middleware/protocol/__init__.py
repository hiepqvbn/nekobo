"""Protocol package for middleware.

This package exposes encoder.encode() and decoder.decode() helpers.
It loads its local `protocol.json` file living in the same folder.
"""
from pathlib import Path
import json
from typing import Dict, Any

_ROOT = Path(__file__).parent
_PROTOCOL_FILE = _ROOT / "protocol.json"


def _load() -> Dict[str, Any]:
    with _PROTOCOL_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


_DATA: Dict[str, Any] = _load()

# convenience exports
messages = _DATA.get('messages', {})
protocol_version = _DATA.get('protocol_version')

def get_messages() -> Dict[str, Any]:
    return messages
