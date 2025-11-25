# app/rag/loaders/api_loader.py
from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

import requests

from app.rag.loaders.base import BaseLoader
from app.resources.schema.rag_schemas import LoadedDocument


def default_json_to_text(data: Any) -> str:
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        return str(data)


class ApiJsonLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__(source_type="api", mime_type="application/json")

    def load(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        response_parser: Optional[Callable[[Any], str]] = None,
        metadata_extra: Optional[Dict[str, Any]] = None,
    ) -> List[LoadedDocument]:
        method_upper = method.upper()
        response_parser = response_parser or default_json_to_text

        self.log(f"Calling API: {method_upper} {url}")

        try:
            resp = requests.request(
                method=method_upper,
                url=url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=timeout,
            )
        except requests.RequestException as e:
            self.log(f"API request error: {e}")
            raise RuntimeError(f"API 요청 실패: {e}") from e

        if not resp.ok:
            self.log(
                f"API response error: status={resp.status_code}, body={resp.text[:200]}"
            )
            raise RuntimeError(
                f"API 응답 오류: status={resp.status_code}, body={resp.text[:500]}"
            )

        # JSON 파싱
        try:
            data = resp.json()
            mime_type = "application/json"
        except ValueError:
            data = resp.text
            mime_type = resp.headers.get("Content-Type", "text/plain")

        # mime_type override
        self.mime_type = mime_type

        text_content = response_parser(data)
        source = self._make_source(None)

        base_meta: Dict[str, Any] = {
            "source": "api",
            "api_url": url,
            "api_method": method_upper,
            "api_params": params or {},
            "api_json_body": json_body or {},
            "status_code": resp.status_code,
        }
        if metadata_extra:
            base_meta.update(metadata_extra)

        return [
            LoadedDocument(
                page_content=text_content,
                metadata=base_meta,
                source=source,
            )
        ]


# 리스트 응답을 item별로 나누는 로더
class ApiItemsLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__(source_type="api", mime_type="application/json")

    def load(
        self,
        url: str,
        *,
        item_path: List[str],
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        item_text_fn: Optional[Callable[[Dict[str, Any]], str]] = None,
        item_metadata_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> List[LoadedDocument]:
        method_upper = method.upper()
        self.log(f"Calling API (items): {method_upper} {url}")

        try:
            resp = requests.request(
                method=method_upper,
                url=url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=timeout,
            )
        except requests.RequestException as e:
            self.log(f"API request error: {e}")
            raise RuntimeError(f"API 요청 실패: {e}") from e

        if not resp.ok:
            self.log(
                f"API response error: status={resp.status_code}, body={resp.text[:200]}"
            )
            raise RuntimeError(
                f"API 응답 오류: status={resp.status_code}, body={resp.text[:500]}"
            )

        try:
            data = resp.json()
        except ValueError:
            raise RuntimeError("API 응답이 JSON 형식이 아닙니다.")

        # item_path 따라 내려가기
        cursor: Any = data
        for key in item_path:
            if not isinstance(cursor, dict) or key not in cursor:
                raise KeyError(f"item_path 중 '{key}' 키를 찾을 수 없습니다.")
            cursor = cursor[key]

        if not isinstance(cursor, list):
            raise TypeError("item_path 위치의 값이 리스트가 아닙니다.")

        items: List[Dict[str, Any]] = cursor
        source = self._make_source(None)

        if item_text_fn is None:

            def _default_item_text_fn(item: Dict[str, Any]) -> str:
                return json.dumps(item, ensure_ascii=False, indent=2)

            item_text_fn = _default_item_text_fn

        if item_metadata_fn is None:

            def _default_item_meta_fn(item: Dict[str, Any]) -> Dict[str, Any]:
                return {}

            item_metadata_fn = _default_item_meta_fn

        docs: List[LoadedDocument] = []
        for idx, item in enumerate(items):
            text = item_text_fn(item)
            meta = {
                "source": "api",
                "api_url": url,
                "api_method": method_upper,
                "item_index": idx,
            }
            meta.update(item_metadata_fn(item))

            docs.append(
                LoadedDocument(
                    page_content=text,
                    metadata=meta,
                    source=source,
                )
            )
        return docs
