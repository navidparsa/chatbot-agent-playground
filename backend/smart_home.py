import json
from config import settings

def build_lamp_tool() -> dict:
    n = settings.lamp_count
    return {
        "type": "function",
        "function": {
            "name": "set_lamps",
            "description": f"Set the on/off state for each of the {n} lamps",
            "parameters": {
                "type": "object",
                "properties": {
                    "states": {
                        "type": "array",
                        "items": {"type": "integer", "enum": [0, 1]},
                        "minItems": n,
                        "maxItems": n,
                        "description": f"Array of {n} values (0=off, 1=on)",
                    }
                },
                "required": ["states"],
            },
        },
    }

def lamp_system_prompt() -> str:
    return (
        f"You control {settings.lamp_count} lamps numbered 1 to {settings.lamp_count}. "
        "Always respond by calling the set_lamps tool."
    )


def all_off() -> list[int]:
    return [0] * settings.lamp_count


def set_lamps(states: list[int]) -> list[int]:
    print(dict(enumerate(states)))
    return states


FUNCTIONS_DICTIONARY = {
    "set_lamps": set_lamps,
}

def extract_tool_call(message: dict):
    tool_calls = message.get("tool_calls")
    if not tool_calls:
        return None
    function = tool_calls[0]["function"]
    if not function:
        return None
    func_name = function["name"]
    arguments = function["arguments"]
    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    return func_name, arguments

