from . import get_messages


def encode(name: str, **kwargs) -> str:
    msgs = get_messages()
    if name not in msgs:
        raise KeyError(f"Unknown message {name}")
    spec = msgs[name]
    id_hex = spec['id']
    args = spec.get('args', [])
    parts = [id_hex]
    for arg in args:
        if arg not in kwargs:
            raise ValueError(f"Missing arg {arg} for message {name}")
        parts.append(str(kwargs[arg]))
    return ' '.join(parts) + '\n'
