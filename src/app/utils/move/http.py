# app/utils/http.py
import httpx
from app.utils.move.exceptions import ExternalAPIError


async def http_get(url: str, params=None, headers=None, timeout=10):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise ExternalAPIError(str(e))


async def http_post(url: str, data=None, json=None, headers=None, timeout=10):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, data=data, json=json, headers=headers)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise ExternalAPIError(str(e))
