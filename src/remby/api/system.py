from typing import List, Optional

from pydantic import TypeAdapter

from remby.api.base import BaseModule
from remby.models.emby.Net import EndPointInfo
from remby.models.emby._internal import PackageVersionInfo, PublicSystemInfo, QueryResultString, SystemInfo, WakeOnLanInfo

class SystemModule(BaseModule):
    def get_system_ping(self) -> str:
        """
        GET /System/Ping

        Ping the Emby API system.

        Returns:
            * **200 OK**: Returns a text string with "Emby Server".
        """
        endpoint = "/System/Ping"
        response = self._client.request("GET", endpoint)
        
        return response.text
    
    def get_system_endpoint(self) -> EndPointInfo:
        """
        GET /System/Endpoint

        Check whether the emby server is in the network or on the local machine.

        Returns:
            * **200 OK**: Returns a dict with is_local and is_in_network.
        """
        endpoint = "/System/Endpoint"
        response = self._client.request("GET", endpoint)
        
        return EndPointInfo.model_validate(response.json())
    
    def get_system_info(self) -> SystemInfo:
        """
        GET /System/Info

        Get api-key-only information about the system Emby is running on.

        Returns:
            * **200 OK**: Returns the api-only-accesible system info.
        """
        endpoint = "/System/Info"
        response = self._client.request("GET", endpoint)
        
        return SystemInfo.model_validate(response.json())
    
    def get_system_info_public(self) -> PublicSystemInfo:
        """
        GET /System/Info/Public

        Get public information about the system Emby is running on.

        Returns:
            * **200 OK**: Returns the publicly available system info.
        """
        endpoint = "/System/Info/Public"
        response = self._client.request("GET", endpoint)
        
        return PublicSystemInfo.model_validate(response.json()) 
    
    def get_system_logs_by_name(self, name: str) -> str:
        """
        GET /System/Logs/{name}

        Get server logs by the specified name.

        Returns:
            * **200 OK**: Returns a text string containing the server logs.
        """
        endpoint = f"/System/Logs/{name}"
        response = self._client.request("GET", endpoint)
        
        return response.text
    
    def get_system_logs_lines_by_name(self, name: str, start_index: int = 0, limit: int = 100) -> QueryResultString:
        """
        GET /System/Logs/{name}/Lines

        Get server logs by the specified name between the lines of `start_index` and `limit`.

        Returns:
            * **200 OK**: Returns a text string containing the server logs between the lines of `start_index` and `limit`.
        
        Notes:
            The Emby documentation does not include the usage of pagination parameters.
            These are however required to prevent returning an empty array!
        """
        endpoint = f"/System/Logs/{name}/Lines"
        response = self._client.request("GET", endpoint, params={
            "StartIndex": start_index,
            "Limit": limit
        })
        
        return QueryResultString.model_validate(response.json())

    def get_system_logs_query(self, start_index: int = 0, limit: int = 100) -> QueryResultString:
        """
        GET /System/Logs/Query

        Get all server logs between the lines of `start_index` and `limit`.

        Returns:
            * **200 OK**: Returns a text string containing all server logs between the lines of `start_index` and `limit`.
        """
        endpoint = f"/System/Logs/Query"
        response = self._client.request("GET", endpoint, params={
            "StartIndex": start_index,
            "Limit": limit
        })
        
        return QueryResultString.model_validate(response.json())

    def get_system_releasenotes(self) -> Optional[PackageVersionInfo]:
        """
        GET /System/ReleaseNotes

        Get a list of all release notes.

        Returns:
            * **200 OK**: Returns a list of all release notes.
            * **204 NO CONTENT**: Returns None if no release notes are available.
        """
        endpoint = f"/System/ReleaseNotes"
        response = self._client.request("GET", endpoint)

        if response.status_code == 204:
            return None
        
        return PackageVersionInfo.model_validate(response.json())
    
    def get_system_releasenotes_versions(self) -> Optional[List[PackageVersionInfo]]:
        """
        GET /System/ReleaseNotes/Versions

        Get a list of all release note versions.

        Returns:
            * **200 OK**: Returns a list of all release note versions.
        """
        endpoint = f"/System/ReleaseNotes/Versions"
        response = self._client.request("GET", endpoint)

        if response.status_code == 204:
            return None

        adapter = TypeAdapter(List[PackageVersionInfo])
        
        return adapter.validate_python(response.json())

    def get_system_wakeonlaninfo(self) -> Optional[List[WakeOnLanInfo]]:
        """
        GET /System/WakeOnLanInfo

        Get a list of WakeOnLan devices.

        Returns:
            * **200 OK**: Returns a list of WakeOnLan devices.
        """
        endpoint = f"/System/WakeOnLanInfo"
        response = self._client.request("GET", endpoint)
        
        if response.status_code == 204:
            return None

        adapter = TypeAdapter(List[WakeOnLanInfo])

        return adapter.validate_python(response.json())

    def head_system_ping(self) -> bool:
        """
        HEAD /System/Ping

        Ping the Emby API system without receiving a response text.\n
        Use this for lightweight up-checking of the Emby server.

        Returns:
            * **200 OK**: Returns the success bool.
        """
        endpoint = f"/System/Ping"
        response = self._client.request("HEAD", endpoint)
        
        return response.status_code == 200

    def post_system_ping(self) -> str:
        """
        POST /System/Ping

        Ping the Emby API system.

        Returns:
            * **200 OK**: Returns a text string with "Emby Server".
        """
        endpoint = "/System/Ping"
        response = self._client.request("POST", endpoint)
        
        return response.text
    
    def post_system_restart(self) -> bool:
        """
        POST /System/Restart

        Restart the server that Emby is running on.

        Returns:
            * **200 OK**: Returns the success bool.
        """
        endpoint = "/System/Restart"
        response = self._client.request("POST", endpoint)
        
        return response.status_code == 200

    def post_system_shutdown(self) -> bool:
        """
        POST /System/Shutdown

        Shut down the server that Emby is running on.

        Returns:
            * **200 OK**: Returns the success bool.
        """
        endpoint = "/System/Shutdown"
        response = self._client.request("POST", endpoint)
        
        return response.status_code == 200
    