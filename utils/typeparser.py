def try_parse_int(string: str) -> int | None:
    try:
        result = int(string)
        return result
    except:
        return None

def try_parse_float(string: str) -> float | None:
    try:
        result = float(string)
        return result
    except:
        return None

def try_parse_bool(string: str) -> bool | None:
    try:
        result = bool(string)
        return result
    except:
        return None
