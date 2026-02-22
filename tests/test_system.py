import json
from pathlib import Path

import pytest
import respx
from httpx import Response
from remby.client import EmbyClient
from remby.exceptions import AuthenticationError
from remby.models.emby._internal import PackageVersionClass

@respx.mock
def test_get_system_ping():
    mock_url = "http://localhost:8096/System/Ping"
    respx.get(mock_url).mock(return_value=Response(200, text="Emby Server"))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_ping()

    assert result == "Emby Server"

@respx.mock
def test_get_system_endpoint():
    mock_url = "http://localhost:8096/System/Endpoint"
    respx.get(mock_url).mock(return_value=Response(200, json={
        "IsLocal": True,
        "IsInNetwork": True,
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_endpoint()

    assert result.is_local is True
    assert result.is_in_network is True

@respx.mock
def test_get_system_endpoint_unauthorized():
    mock_url = "http://localhost:8096/System/Endpoint"
    respx.get(mock_url).mock(return_value=Response(401, text="Unauthorized"))

    with EmbyClient(base_url="http://localhost:8096", api_key="invalid_token") as client:
        with pytest.raises(AuthenticationError) as exc_info:
            client.system.get_system_endpoint()
        
        assert "Authentication failed" in str(exc_info.value)

@respx.mock
def test_get_system_info():
    fixture_path = Path(__file__).parent / "fixtures" / "system_info.json"
    mock_payload = json.loads(fixture_path.read_text())

    mock_url = "http://localhost:8096/System/Info"
    respx.get(mock_url).mock(return_value=Response(200, json=mock_payload))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_info()

    assert result is not None 
    
    assert result.system_update_level == PackageVersionClass(root="Release")
    
    assert result.completed_installations is not None
    assert len(result.completed_installations) == 1
    assert result.completed_installations[0].name == "Installation"

@respx.mock
def test_get_system_info_public():
    mock_url = "http://localhost:8096/System/Info/Public"
    respx.get(mock_url).mock(return_value=Response(200, json={
        "LocalAddress": "127.0.0.1",
        "LocalAddresses": ["127.0.0.1"],
        "WanAddress": "127.0.0.1",
        "RemoteAddresses": [],
        "ServerName": "Server",
        "Version": "1.0.0",
        "Id": "1"
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_info_public()

    assert result.local_address == "127.0.0.1"
    assert result.local_addresses is not None
    assert len(result.local_addresses) == 1
    assert result.server_name == "Server"

@respx.mock
def test_get_system_logs_by_name():
    target_log = "embyserver.txt"
    mock_url = f"http://localhost:8096/System/Logs/{target_log}"
    
    respx.get(mock_url).mock(return_value=Response(200, text="2026-02-21 21:00:00.000 Info Main: Test Log Line..."))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_logs_by_name(name=target_log)

    assert "Test Log Line..." in result
    assert isinstance(result, str)

@respx.mock
def test_get_system_logs_line_by_name():
    target_log = "embyserver.txt"
    mock_url = f"http://localhost:8096/System/Logs/{target_log}/Lines"
    
    respx.get(mock_url).mock(return_value=Response(200, json={
        "Items": [
            "2026-02-21 21:00:00 Info: Line 1",
            "2026-02-21 21:00:01 Info: Line 2"
        ],
        "TotalRecordCount": 2
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_logs_lines_by_name(name=target_log)

    assert result is not None
    assert result.items is not None
    assert result.total_record_count == 2
    assert len(result.items) == 2

@respx.mock
def test_get_system_logs_query():
    mock_url = f"http://localhost:8096/System/Logs/Query"
    
    respx.get(mock_url).mock(return_value=Response(200, json={
        "Items": [
            "2026-02-21 21:00:00 Info: Line 1",
            "2026-02-21 21:00:01 Info: Line 2"
        ],
        "TotalRecordCount": 2
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_logs_query()

    assert result is not None
    assert result.items is not None
    assert result.total_record_count == 2
    assert len(result.items) == 2

@respx.mock
def test_get_system_releasenotes_no_content():
    mock_url = f"http://localhost:8096/System/ReleaseNotes"
    
    respx.get(mock_url).mock(return_value=Response(204))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_releasenotes()

    assert result is None

@respx.mock
def test_get_system_releasenotes():
    mock_url = f"http://localhost:8096/System/ReleaseNotes"
    
    respx.get(mock_url).mock(return_value=Response(200, json={
        "versionStr": "1.0.0",
        "description": "Initial Release"
    }))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_releasenotes()

    assert result is not None
    assert result.version_str == "1.0.0"
    assert result.description == "Initial Release"

@respx.mock
def test_get_system_releasenotes_versions():
    mock_url = f"http://localhost:8096/System/ReleaseNotes/Versions"
    
    respx.get(mock_url).mock(return_value=Response(200, json=[
        {
            "name": "1.0.0-Beta",
            "versionStr": "1.0.0",
            "classification": "Beta"
        },
    ]))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_releasenotes_versions()

    assert result is not None
    assert len(result) == 1

    assert result[0].name == "1.0.0-Beta"
    assert result[0].version_str == "1.0.0"
    assert result[0].classification == PackageVersionClass(root="Beta")

@respx.mock
def test_get_system_wakeonlaninfo():
    mock_url = f"http://localhost:8096/System/WakeOnLanInfo"
    
    respx.get(mock_url).mock(return_value=Response(200, json=[
        {
            "MacAddress": "0A0A0A0A0A0A",
            "BroadcastAddress": "255.255.255.255",
            "Port": 9
        },
    ]))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.get_system_wakeonlaninfo()

    assert result is not None
    assert len(result) == 1

    assert result[0].mac_address == "0A0A0A0A0A0A"
    assert result[0].broadcast_address == "255.255.255.255"
    assert result[0].port == 9

@respx.mock
def test_head_system_ping():
    mock_url = "http://localhost:8096/System/Ping"
    respx.head(mock_url).mock(return_value=Response(200, text="Emby Server"))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.head_system_ping()

    assert result is True

@respx.mock
def test_post_system_ping():
    mock_url = "http://localhost:8096/System/Ping"
    respx.post(mock_url).mock(return_value=Response(200, text="Emby Server"))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.post_system_ping()

    assert result == "Emby Server"

@respx.mock
def test_post_system_restart():
    mock_url = "http://localhost:8096/System/Restart"
    respx.post(mock_url).mock(return_value=Response(200, text="Emby Server"))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.post_system_restart()

    assert result is True

@respx.mock
def test_post_system_shutdown():
    mock_url = "http://localhost:8096/System/Shutdown"
    respx.post(mock_url).mock(return_value=Response(200, text="Emby Server"))

    with EmbyClient(base_url="http://localhost:8096", api_key="dummy") as client:
        result = client.system.post_system_shutdown()

    assert result is True