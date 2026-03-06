import json
from pathlib import Path

from httpx import Response
import respx

from remby._client import EmbyClient


@respx.mock
def test_get_users_public():
    fixture_path = Path(__file__).parent / "fixtures" / "user_dto.json"
    mock_payload = json.loads(fixture_path.read_text())

    mock_url = "http://localhost:8096/Users/Public"
    respx.get(mock_url).mock(return_value=Response(200, json=[mock_payload]))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.users.get_users_public()
    
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].id == "id123"
    assert result.data[0].server_name == "serverName"

@respx.mock
def test_get_users_by_id():
    fixture_path = Path(__file__).parent / "fixtures" / "user_dto.json"
    mock_payload = json.loads(fixture_path.read_text())

    mock_url = "http://localhost:8096/Users/1"
    respx.get(mock_url).mock(return_value=Response(200, json=mock_payload))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.users.get_users_by_id("1")
    
    assert result.data is not None
    assert result.data.id == "id123"
    assert result.data.server_name == "serverName"