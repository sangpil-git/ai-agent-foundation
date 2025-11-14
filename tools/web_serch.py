from langchain_core.tools import tool


# 실제로는 Tavily, SerpAPI, 사내 검색 API 등으로 교체 가능
@tool("web_search")
def web_search(query: str) -> str:
    """
    (Stub) 실제 검색 API와 연계 예정.
    지금은 설명용 더미를 반환.
    """
    return f"[stub] 검색 결과 요약 for: {query}"
