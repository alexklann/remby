from typing import List

from remby._api.base import BaseModule
from remby.models.emby._internal import QueryResultUserDto, UserDto
from remby.models.response import EmbyResponse
from remby.models.user import GetUsersRequest


class UsersModule(BaseModule):
    def get_users_public(self) -> EmbyResponse[List[UserDto]]:
        endpoint = "/Users/Public"
        response = self._client.request("GET", endpoint)
        data = [UserDto.model_validate(item) for item in response.json()]
        return EmbyResponse.from_httpx(response, data)
    
    def get_users_by_id(self, user_id: str) -> EmbyResponse[UserDto]:
        endpoint = f"/Users/{user_id}"
        response = self._client.request("GET", endpoint)
        data = UserDto.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)

    def get_users_query(self, query: GetUsersRequest) -> EmbyResponse[QueryResultUserDto]:
        endpoint = f"/Users/Query"
        response = self._client.request("GET", endpoint, params=query.model_dump(by_alias=True, exclude_none=True))
        data = UserDto.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)