from typing import TypedDict, List
from langchain_core.tools import BaseTool


class PlanState(TypedDict):
    user_input: str
    plan: str
    steps: List[str]
    result: str


def plan_node(state: PlanState) -> PlanState:
    # TODO: LLM 사용해서 작업 플랜 생성
    # ex) "1) 정보 조회, 2) 요약, 3) 결과 정리"
    return {
        **state,
        "plan": "1) 정보 조회\n2) 요약\n3) 결과 정리",
        "steps": ["정보 조회", "요약", "결과 정리"],
    }


def act_node(state: PlanState) -> PlanState:
    # TODO: tools 사용 (web_search, db_knowledge 등)
    return {
        **state,
        "result": f"플랜을 따라 수행된 결과 (stub). plan: {state['plan']}",
    }
