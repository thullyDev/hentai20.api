import asyncio
import requests
from typing import Dict, Any, Union
from ..resources import SUCCESSFUL

class ApiHandler:
    def __init__(self, BASE: str):
        self.BASE = BASE

    async def request(self, endpoint: str, method: str = 'GET', image: bool = False, html: bool = False, **kwargs: Any) -> Union[Dict[str, Any], str, int, bytes]:
        url = self.BASE + endpoint
        response = requests.request(method, url, **kwargs)
        status_code: int = response.status_code

        if status_code != SUCCESSFUL:
            return status_code
            
        if image:
            return response.content

        if html:
            return response.text

        return response.json()

    async def get(self, endpoint: str, *, params: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str, int, bytes]:
        return await self.request(endpoint, params=params, method='GET', **kwargs)

    async def post(self, endpoint: str, *, data: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str, int, bytes]:
        return await self.request(endpoint, data=data, method='POST', **kwargs)

    async def put(self, endpoint: str, *, data: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str, int, bytes]:
        return await self.request(endpoint, data=data, method='PUT', **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> Union[Dict[str, Any], str, int, bytes]:
        return await self.request(endpoint, method='DELETE', **kwargs)