from langchain_core.tools import tool


@tool("calculator", return_direct=False)
def calculator(expression: str) -> str:
    """
    간단한 수식 계산기.
    예: "1 + 2 * 3"
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"
