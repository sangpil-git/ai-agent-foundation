from langgraph.graph import StateGraph, END
from planner_executor.nodes import PlanState, plan_node, act_node


def build_planner_executor_graph():
    graph = StateGraph(PlanState)
    graph.add_node("plan", plan_node)
    graph.add_node("act", act_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "act")
    graph.add_edge("act", END)

    return graph.compile()
