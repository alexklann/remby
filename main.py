import remby
import remby.client
from remby.models.items import GetItemRequest

remby_client = remby.client.EmbyClient("http://192.168.1.111:8096/", "f3433d8b430348b7bff735bf8220939a")

found_items = remby_client.items.get_items(GetItemRequest(recursive=True, artists="Michael Jackson"))
if not found_items.items: exit(1)
for item in found_items.items:
    if item.type == "MusicAlbum":
        print(item.name)