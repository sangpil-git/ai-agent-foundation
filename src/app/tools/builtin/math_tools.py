# app/tools/builtin/math_tools.py
from app.tools.base import registered_tool


@registered_tool("add_numbers", return_direct=True)
def add_numbers(a: float, b: float) -> float:
    """두 숫자의 합을 반환"""
    return float(a) + float(b)


@registered_tool("multiply", return_direct=True)
def multiply(a: float, b: float) -> float:
    """두 숫자의 곱을 반환"""
    return float(a) * float(b)
