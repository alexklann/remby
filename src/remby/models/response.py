from typing import Generic, TypeVar
from pydantic import BaseModel
import httpx

T = TypeVar("T")

class EmbyResponse(BaseModel, Generic[T]):
    data: T
    status_code: int
    headers: dict[str, str]

    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def from_httpx(cls, response: httpx.Response, data: T) -> "EmbyResponse[T]":
        return cls(
            data=data,
            status_code=response.status_code,
            headers=dict(response.headers),
        )