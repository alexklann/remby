from remby.api.base import BaseModule
from remby.models.emby._internal import QueryResultBaseItemDto
from remby.models.items import GetItemRequest

class ItemsModule(BaseModule):
    def get_items(self, query: GetItemRequest) -> QueryResultBaseItemDto:
        """
        GET /Items

        Get an item based on a query.

        Returns:
            * **200 OK**: Returns the fetched object.
        """
        query_params = query.model_dump(by_alias=True, exclude_none=True)

        endpoint = "/Items"
        response = self._client.request("GET", endpoint, params=query_params)
        
        return QueryResultBaseItemDto.model_validate(response.json())
    
    def get_users_by_userid_items(self, user_id: str, query: GetItemRequest) -> QueryResultBaseItemDto:
        """
        GET /Users/{UserId}/Items

        Appears to get items for a specific user account by UserId.

        Returns:
            * **200 OK**: Returns a list of items associated with this user.
        """
        query_params = query.model_dump(by_alias=True, exclude_none=True)

        endpoint = f"/Users/{user_id}/Items"
        response = self._client.request("GET", endpoint, params=query_params)
        
        return QueryResultBaseItemDto.model_validate(response.json())
    
    def get_users_by_userid_items_resume(self, user_id: str, query: GetItemRequest) -> QueryResultBaseItemDto:
        """
        GET /Users/{UserId}/Items

        Gets items that are on the "Continue Watching" list for a specific user.

        Returns:
            * **200 OK**: Returns a list of items on resume.
        """
        query_params = query.model_dump(by_alias=True, exclude_none=True)

        endpoint = f"/Users/{user_id}/Items/Resume"
        response = self._client.request("GET", endpoint, params=query_params)
        
        return QueryResultBaseItemDto.model_validate(response.json())