from langchain_core.messages import AIMessage
from tools.rag_tools import search_maintenance_knowledge


def knowledge_agent(state: dict) -> dict:
    symptoms = state["symptoms"]
    diagnostic_findings = state.get("diagnostic_findings", "")

    query = f"{symptoms} {diagnostic_findings[:200]}"

    results = search_maintenance_knowledge(query)

    summary = f"Retrieved {len(results)} relevant sections from maintenance manuals."

    return {
        "knowledge_retrieved": results,
        "messages": [AIMessage(content=f"Knowledge: {summary}")],
        "next_agent": "hitl"
    }