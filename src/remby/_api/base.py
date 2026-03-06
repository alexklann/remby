from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from remby._client import EmbyClient

class BaseModule:
    def __init__(self, client: "EmbyClient") -> None:
        self._client = client