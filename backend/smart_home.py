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


LAMP_TOOL = build_lamp_tool()


def lamp_system_prompt() -> str:
    return (
        f"You control {settings.lamp_count} lamps numbered 1 to {settings.lamp_count}. "
        "Always respond by calling the set_lamps tool."
    )


def all_off() -> list[int]:
    return [0] * settings.lamp_count


def extract_states(msg: dict) -> list[int] | None:
    tool_calls = msg.get("tool_calls")
    if not tool_calls:
        return None
    args = tool_calls[0]["function"]["arguments"]
    if isinstance(args, str):
        args = json.loads(args)
    return args.get("states")
