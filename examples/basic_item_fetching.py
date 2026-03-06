import os
from remby import EmbyClient, GetItemRequest

base_url = os.environ.get("EMBY_BASE_URL", "")

remby_client = EmbyClient(base_url, "f3433d8b430348b7bff735bf8220939a")

found_items = remby_client.items.get_items(GetItemRequest(recursive=True, artists="Michael Jackson"))
if not found_items.data.items: exit(1)
for item in found_items.data.items:
    if item.type == "MusicAlbum":
        print(item.name)