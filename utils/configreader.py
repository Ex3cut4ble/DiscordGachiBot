from utils.typeparser import *


class Config:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._config_values = dict()
        self._parse_config()

    def _parse_config(self):
        with open(self._filepath, 'r') as configfile:
            for line in configfile:
                key, arg = line.split("=", 1)
                arg = arg.strip()
                if arg.startswith("\"") or arg.startswith("\'"):
                    self._config_values[key] = arg[1:-1]
                elif try_parse_float(arg) is not None:
                    self._config_values[key] = try_parse_float(arg)
                elif try_parse_int(arg) is not None:
                    self._config_values[key] = try_parse_int(arg)
                elif try_parse_bool(arg) is not None:
                    self._config_values[key] = try_parse_bool(arg)
                else:
                    raise Exception("Unknown value type found in config.")

    def get_value(self, key: str) -> str | int | float | bool:
        value = self._config_values[key]
        if value is None:
            raise Exception(f"Value with key \"{key}\" not found in config.")

        return value