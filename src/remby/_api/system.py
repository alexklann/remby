from typing import List, Optional

from pydantic import TypeAdapter

from remby._api.base import BaseModule
from remby.models.emby.Net import EndPointInfo
from remby.models.emby._internal import PackageVersionInfo, PublicSystemInfo, QueryResultString, SystemInfo, WakeOnLanInfo
from remby.models.response import EmbyResponse

class SystemModule(BaseModule):
    def get_system_ping(self) -> str:
        endpoint = "/System/Ping"
        response = self._client.request("GET", endpoint)
        
        return response.text
    
    def get_system_endpoint(self) -> EmbyResponse[EndPointInfo]:
        endpoint = "/System/Endpoint"
        response = self._client.request("GET", endpoint)
        data = EndPointInfo.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)
    
    def get_system_info(self) -> EmbyResponse[SystemInfo]:
        endpoint = "/System/Info"
        response = self._client.request("GET", endpoint)
        data = SystemInfo.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)
    
    def get_system_info_public(self) -> EmbyResponse[PublicSystemInfo]:
        endpoint = "/System/Info/Public"
        response = self._client.request("GET", endpoint)
        data = PublicSystemInfo.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)
    
    def get_system_logs_by_name(self, name: str) -> str:
        endpoint = f"/System/Logs/{name}"
        response = self._client.request("GET", endpoint)
        
        return response.text
    
    def get_system_logs_lines_by_name(self, name: str, start_index: int = 0, limit: int = 100) -> EmbyResponse[QueryResultString]:
        """
        The Emby documentation does not include the usage of pagination parameters.
        These are however required to prevent returning an empty array!
        """
        endpoint = f"/System/Logs/{name}/Lines"
        response = self._client.request("GET", endpoint, params={
            "StartIndex": start_index,
            "Limit": limit
        })
        
        data = QueryResultString.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)

    def get_system_logs_query(self, start_index: int = 0, limit: int = 100) -> EmbyResponse[QueryResultString]:
        endpoint = f"/System/Logs/Query"
        response = self._client.request("GET", endpoint, params={
            "StartIndex": start_index,
            "Limit": limit
        })
        
        data = QueryResultString.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)

    def get_system_releasenotes(self) -> EmbyResponse[Optional[PackageVersionInfo]]:
        endpoint = f"/System/ReleaseNotes"
        response = self._client.request("GET", endpoint)

        if response.status_code == 204:
            return EmbyResponse.from_httpx(response, None)
        
        data = PackageVersionInfo.model_validate(response.json())
        return EmbyResponse.from_httpx(response, data)
    
    def get_system_releasenotes_versions(self) -> EmbyResponse[Optional[List[PackageVersionInfo]]]:
        endpoint = f"/System/ReleaseNotes/Versions"
        response = self._client.request("GET", endpoint)

        if response.status_code == 204:
            return EmbyResponse.from_httpx(response, None)

        adapter = TypeAdapter(List[PackageVersionInfo])
        data = adapter.validate_python(response.json())
        return EmbyResponse.from_httpx(response, data)

    def get_system_wakeonlaninfo(self) -> EmbyResponse[Optional[List[WakeOnLanInfo]]]:
        endpoint = f"/System/WakeOnLanInfo"
        response = self._client.request("GET", endpoint)
        
        if response.status_code == 204:
            return EmbyResponse.from_httpx(response, None)

        adapter = TypeAdapter(List[WakeOnLanInfo])
        data = adapter.validate_python(response.json())
        return EmbyResponse.from_httpx(response, data)

    def head_system_ping(self) -> bool:
        endpoint = f"/System/Ping"
        response = self._client.request("HEAD", endpoint)
        
        return response.status_code == 200

    def post_system_ping(self) -> str:
        endpoint = "/System/Ping"
        response = self._client.request("POST", endpoint)
        
        return response.text
    
    def post_system_restart(self) -> bool:
        endpoint = "/System/Restart"
        response = self._client.request("POST", endpoint)
        
        return response.status_code == 200

    def post_system_shutdown(self) -> bool:
        endpoint = "/System/Shutdown"
        response = self._client.request("POST", endpoint)
        
        return response.status_code == 200
    