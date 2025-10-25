from . import get_messages
from typing import Any, Dict


def decode(raw: str) -> Dict[str, Any] | None:
    if raw is None:
        return None
    line = raw.strip()
    if not line:
        return None

    toks = line.split()
    idtok = toks[0]

    # find name by id
    msgs = get_messages()
    name = None
    for n, spec in msgs.items():
        if spec.get('id') == idtok:
            name = n
            break

    if not name:
        return {'raw': line}

    spec = msgs[name]
    args = spec.get('args', [])
    vals = toks[1:]
    out: Dict[str, Any] = {'name': name, 'id': idtok}
    for i, arg in enumerate(args):
        if i < len(vals):
            try:
                v = int(vals[i])
            except Exception:
                v = vals[i]
        else:
            v = None
        out[arg] = v
    return out
