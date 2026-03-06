from pathlib import Path

import respx
from httpx import Response
from remby import EmbyClient
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
    assert result.data.items is not None

    assert len(result.data.items) == 1
    assert result.data.items[0].id == "12345"
    assert result.data.items[0].name == "Bad"
    assert isinstance(result.data.items[0], BaseItemDto)

@respx.mock
def test_iter_items_multi_page():    
    mock_url = "http://localhost:8096/Items"
    
    route1 = respx.get(mock_url, params={"StartIndex": "0"}).mock(
        return_value=Response(200, json={
            "Items": [{"Name": "Page1-Item", "Id": "1"}],
            "TotalRecordCount": 2
        })
    )

    route2 = respx.get(mock_url, params={"StartIndex": "1"}).mock(
        return_value=Response(200, json={
            "Items": [{"Name": "Page2-Item", "Id": "2"}],
            "TotalRecordCount": 2
        })
    )

    with EmbyClient(base_url="http://localhost:8096", api_key="test") as client:
        items = list(client.items.iter_items(GetItemRequest(recursive=True), page_size=1))

    assert len(items) == 2
    assert items[0].name == "Page1-Item"
    assert items[1].name == "Page2-Item"
    assert route1.called
    assert route2.called

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
    assert result.data.items is not None

    assert len(result.data.items) == 1
    assert result.data.items[0].id == "12345"
    assert result.data.items[0].name == "Bad"
    assert isinstance(result.data.items[0], BaseItemDto)

@respx.mock
def test_iter_items_by_userid_multi_page():    
    mock_url = "http://localhost:8096/Users/1/Items"
    
    route1 = respx.get(mock_url, params={"StartIndex": "0"}).mock(
        return_value=Response(200, json={
            "Items": [{"Name": "Page1-Item", "Id": "1"}],
            "TotalRecordCount": 2
        })
    )

    route2 = respx.get(mock_url, params={"StartIndex": "1"}).mock(
        return_value=Response(200, json={
            "Items": [{"Name": "Page2-Item", "Id": "2"}],
            "TotalRecordCount": 2
        })
    )

    with EmbyClient(base_url="http://localhost:8096", api_key="test") as client:
        items = list(client.items.iter_items_by_userid("1", GetItemRequest(recursive=True), page_size=1))

    assert len(items) == 2
    assert items[0].name == "Page1-Item"
    assert items[1].name == "Page2-Item"
    assert route1.called
    assert route2.called

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
    assert result.data.items is not None

    assert len(result.data.items) == 1
    assert result.data.items[0].id == "12345"
    assert result.data.items[0].name == "Bad"
    assert isinstance(result.data.items[0], BaseItemDto)