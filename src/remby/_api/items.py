from typing import Any, Callable, Iterator

from remby._api.base import BaseModule
from remby.models.emby._internal import BaseItemDto, QueryResultBaseItemDto
from remby.models.items import GetItemRequest
from remby.models.response import EmbyResponse

def _paginate_items(fetch: Callable[..., Any], start: int = 0, page_size: int = 50, max_items: int | None = None) -> Iterator[BaseItemDto]:
    yielded = 0
    while True:
        limit = page_size
        if max_items:
            limit = min(page_size, max_items - yielded)
        result = fetch(start, limit).data
        
        if not result.items:
            return
        
        for item in result.items:
            yield item
            yielded += 1
            if max_items and yielded >= max_items:
                return

        start += len(result.items)

        if result.total_record_count and start >= result.total_record_count:
            return

class ItemsModule(BaseModule):
    def get_items(self, query: GetItemRequest) -> EmbyResponse[QueryResultBaseItemDto]:
        """
        GET /Items

        Get an item based on a query.

        Returns:
            * **200 OK**: Returns the fetched object.
        """
        endpoint = "/Items"
        response = self._client.request("GET", endpoint, params=query.model_dump(by_alias=True, exclude_none=True))
        data = QueryResultBaseItemDto.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)
    
    def iter_items(self, query: GetItemRequest, start: int = 0, page_size: int = 50, max_items: int | None = None) -> Iterator[BaseItemDto]:
        yield from _paginate_items(
            fetch=lambda start, limit: self.get_items(
                query.model_copy(update={"start_index": start, "limit": limit})
            ),
            start=start,
            page_size=page_size,
            max_items = max_items
        )
    
    def get_users_by_userid_items(self, user_id: str, query: GetItemRequest) -> EmbyResponse[QueryResultBaseItemDto]:
        """
        GET /Users/{UserId}/Items

        Appears to get items for a specific user account by UserId.

        Returns:
            * **200 OK**: Returns a list of items associated with this user.
        """
        endpoint = f"/Users/{user_id}/Items"
        response = self._client.request("GET", endpoint, params=query.model_dump(by_alias=True, exclude_none=True))
        data = QueryResultBaseItemDto.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)

    def iter_items_by_userid(self, user_id: str, query: GetItemRequest, start: int = 0, page_size: int = 50, max_items: int | None = None) -> Iterator[BaseItemDto]:
        yield from _paginate_items(
            fetch=lambda start, limit: self.get_users_by_userid_items(
                user_id,
                query.model_copy(update={"start_index": start, "limit": limit})
            ),
            start=start,
            page_size=page_size,
            max_items = max_items
        )
    
    def get_users_by_userid_items_resume(self, user_id: str, query: GetItemRequest) -> EmbyResponse[QueryResultBaseItemDto]:
        """
        GET /Users/{UserId}/Items

        Gets items that are on the "Continue Watching" list for a specific user.

        Returns:
            * **200 OK**: Returns a list of items on resume.
        """
        endpoint = f"/Users/{user_id}/Items/Resume"
        response = self._client.request("GET", endpoint, params=query.model_dump(by_alias=True, exclude_none=True))
        data = QueryResultBaseItemDto.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)

    def iter_items_by_userid_resume(self, user_id: str, query: GetItemRequest, start: int = 0, page_size: int = 50, max_items: int | None = None) -> Iterator[BaseItemDto]:
        yield from _paginate_items(
            fetch=lambda start, limit: self.get_users_by_userid_items_resume(
                user_id,
                query.model_copy(update={"start_index": start, "limit": limit})
            ),
            start=start,
            page_size=page_size,
            max_items = max_items
        )