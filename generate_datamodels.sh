#!/bin/bash
uv run datamodel-codegen \
  --input openapi.json \
  --input-file-type openapi \
  --output src/remby/models/emby \
  --output-model-type pydantic_v2.BaseModel \
  --target-python-version 3.12 \
  --use-standard-collections \
  --use-schema-description \
  --use-double-quotes \
  --enum-field-as-literal all