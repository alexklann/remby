from pathlib import Path

import respx
from httpx import Response
from remby.client import EmbyClient
from remby.models.emby._internal import BaseItemDto
from remby.models.items import GetItemRequest

@respx.mock
def test_get_items():    
    mock_url = "http://localhost:8096/Items"
    respx.get(mock_url).mock(return_value=Response(200, json={
        "Items": [
            {
                "Name": "Bad",
                "Id": "12345",
                "Type": "MusicAlbum"
            }
        ],
        "TotalRecordCount": 1
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="test") as client:
        result = client.items.get_items(GetItemRequest(recursive=True, artists="Michael Jackson"))

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1
    assert result.items[0].id == "12345"
    assert result.items[0].name == "Bad"
    assert isinstance(result.items[0], BaseItemDto)

@respx.mock
def test_get_users_by_userid_items():    
    mock_url = "http://localhost:8096/Users/1/Items"
    respx.get(mock_url).mock(return_value=Response(200, json={
        "Items": [
            {
                "Name": "Bad",
                "Id": "12345",
                "Type": "MusicAlbum"
            }
        ],
        "TotalRecordCount": 1
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="test") as client:
        result = client.items.get_users_by_userid_items(user_id="1", query=GetItemRequest(recursive=True, artists="Michael Jackson"))

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1
    assert result.items[0].id == "12345"
    assert result.items[0].name == "Bad"
    assert isinstance(result.items[0], BaseItemDto)

@respx.mock
def test_get_users_by_userid_items_resume():    
    mock_url = "http://localhost:8096/Users/1/Items/Resume"
    respx.get(mock_url).mock(return_value=Response(200, json={
        "Items": [
            {
                "Name": "Bad",
                "Id": "12345",
                "Type": "MusicAlbum"
            }
        ],
        "TotalRecordCount": 1
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="test") as client:
        result = client.items.get_users_by_userid_items_resume(user_id="1", query=GetItemRequest(recursive=True, artists="Michael Jackson"))

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1
    assert result.items[0].id == "12345"
    assert result.items[0].name == "Bad"
    assert isinstance(result.items[0], BaseItemDto)