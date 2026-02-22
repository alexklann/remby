# param_converter.py
# version 1.0
#
# A small script to convert openapi.json param arrays into pydantic classes
# Make sure the file is called params.json and it's just a plain array with dicts, so:
# [{...}, {...}]

import json, re

CLASS_NAME = "GetItemRequest"

def pascal_to_snake(name_pascal: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name_pascal).lower()

with open("params.json", "r", encoding="UTF-8") as f:
    final_class_fields = [f"class {CLASS_NAME}(BaseModel):\n", "    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)\n"]
    json_contents = json.load(f)
    for item in json_contents:
        name_pascal = item["name"]
        name_snake = pascal_to_snake(name_pascal)
        item_type = None
        match item["schema"]["type"].lower():
            case "integer":
                item_type = "int"
            case "number":
                item_type = "int"
            case "string":
                item_type = "str"
            case "boolean":
                item_type = "bool"
        final_class_fields.append(f'    {name_snake}: {item_type} | None = Field(default=None)\n')
    with open("class.py", "w") as c:
        c.writelines(final_class_fields)