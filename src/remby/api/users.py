from typing import List

from remby.api.base import BaseModule
from remby.models.emby._internal import UserDto


class UsersModule(BaseModule):
    def get_users_public(self, **params) -> List[UserDto]:
        """
        GET /Users/Public

        Get an item based on the user query.

        Returns:
            * **200 OK**: Returns the parsed list of User objects.
        """
        endpoint = "/Users/Public"
        response = self._client.request("GET", endpoint, params=params)
        
        return [UserDto.model_validate(item) for item in response.json()]