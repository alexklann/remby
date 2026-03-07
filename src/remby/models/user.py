from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_pascal


class GetUsersRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)
    is_hidden: bool | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)
    start_index: int | None = Field(default=None)
    limit: int | None = Field(default=None)
    name_starts_with_or_greater: str | None = Field(default=None)
    sort_order: Literal['Ascending', 'Descending'] | None = Field(default=None)