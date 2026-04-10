from langgraph.graph import StateGraph, END
from graph.state import MaintenanceState
from graph.checkpointer import get_checkpointer
from agents.planner import planner_agent
from agents.data_retrieval import data_retrieval_agent
from agents.diagnostic import diagnostic_agent
from agents.knowledge_agent import knowledge_agent
from agents.hitl import hitl_agent
from agents.report_writer import report_writer_agent


def route_after_supervisor(state: dict) -> str:
    next_agent = state.get("next_agent", "end")
    retry_count = state.get("retry_count", 0)
    error = state.get("error", None)

    if error:
        return END
    if next_agent == "end":
        return END
    return next_agent


def build_graph():
    graph = StateGraph(MaintenanceState)

    graph.add_node("planner", planner_agent)
    graph.add_node("data_retrieval", data_retrieval_agent)
    graph.add_node("diagnostic", diagnostic_agent)
    graph.add_node("knowledge", knowledge_agent)
    graph.add_node("hitl", hitl_agent)
    graph.add_node("report_writer", report_writer_agent)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "data_retrieval")
    graph.add_edge("data_retrieval", "diagnostic")
    graph.add_edge("diagnostic", "knowledge")
    graph.add_edge("knowledge", "hitl")

    graph.add_conditional_edges(
        "hitl",
        route_after_supervisor,
        {
            "diagnostic": "diagnostic",
            "report_writer": "report_writer",
            END: END
        }
    )

    graph.add_edge("report_writer", END)

    checkpointer = get_checkpointer()
    return graph.compile(checkpointer=checkpointer)