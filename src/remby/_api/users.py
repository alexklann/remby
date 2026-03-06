from typing import List

from remby._api.base import BaseModule
from remby.models.emby._internal import UserDto
from remby.models.response import EmbyResponse


class UsersModule(BaseModule):
    def get_users_public(self) -> EmbyResponse[List[UserDto]]:
        """
        GET /Users/Public

        Get all public users.

        Returns:
            * **200 OK**: Returns the parsed list of User objects.
        """
        endpoint = "/Users/Public"
        response = self._client.request("GET", endpoint)
        data = [UserDto.model_validate(item) for item in response.json()]
        return EmbyResponse.from_httpx(response, data)
    
    def get_users_by_id(self, user_id: str) -> EmbyResponse[UserDto]:
        """
        GET /Users/{Id}

        Get a user by id.

        Returns:
            * **200 OK**: Returns the User object.
        """
        endpoint = f"/Users/{user_id}"
        response = self._client.request("GET", endpoint)
        data = UserDto.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)