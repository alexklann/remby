from typing import Any

import httpx

from remby.api.items import ItemsModule
from remby.api.users import UsersModule
from remby.exceptions import AuthenticationError, EmbyException
from remby.api.system import SystemModule

class EmbyClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key
        
        self._session = httpx.Client(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "X-Emby-Token": self.api_key
            },
            timeout=10.0,
        )
        
        self.system = SystemModule(self)
        self.items = ItemsModule(self)
        self.users = UsersModule(self)
    
    def request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        try:
            response = self._session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):
                raise AuthenticationError(f"Authentication failed: {e.response.text}") from e
            raise EmbyException(f"HTTP Status Error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise EmbyException(f"Network or routing error occurred: {e}") from e

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "EmbyClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()