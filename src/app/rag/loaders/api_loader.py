# app/rag/loaders/api_loader.py
"""
REST/JSON API 응답을 텍스트 문서로 변환하는 예시 로더.
"""
from typing import Any, Dict, List


def load_from_api_response(data: Dict[str, Any]) -> List[str]:
    """
    API 응답(JSON dict)을 받아서 문서 텍스트 리스트로 변환.
    실제 구현은 도메인에 맞게 커스터마이징.
    """
    # TODO: key/value 조합, 특정 필드를 concat 하는 형태로 구현
    return [str(data)]
