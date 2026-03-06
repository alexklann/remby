# fixture_generator.py
# version 1.0
#
# This converts the parameters from an open_api.json file
# into a pre-filled mockable fixture. The script does not auto-resolve refs.
# Arrays have to be populated manually (they're marked with "MISSING#ARRAY").
# The input file should be a plain json with the following format:
#
# {
#   "properties": {
#       ...
#   }
# }

import json, re
from typing import Any

def pascal_to_snake(name_pascal: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name_pascal).lower()

def generate_mock_contents(key: str, input_dict: dict) -> Any:
    type = "ref"
    if "type" in input_dict.keys():
        type = input_dict["type"]
    match type:
        case "array":
            return "MISSING#ARRAY"
        case "string":
            return pascal_to_snake(key)
        case "integer":
            return 123
        case "boolean":
            return True
        case "ref":
            return input_dict["$ref"]

with open("params.json", "r", encoding="UTF-8") as f:
    final_json = {}
    json_contents = json.load(f)
    dict_keys = list(json_contents["properties"].keys())
    for key in dict_keys:
        final_json[key] = str(generate_mock_contents(key, json_contents["properties"][key]))
    with open("final_fixture.json", "w") as fix:
        json.dump(final_json, fix, indent=4)