from langgraph.types import interrupt
from langchain_core.messages import AIMessage


def hitl_agent(state: dict) -> dict:
    equipment_id = state["equipment_id"]
    diagnostic_findings = state.get("diagnostic_findings", "No diagnosis available")
    knowledge_retrieved = state.get("knowledge_retrieved", [])
    retry_count = state.get("retry_count", 0)

    knowledge_summary = "\n".join([
        item["content"][:200] for item in knowledge_retrieved
    ]) if knowledge_retrieved else "No manual references found"

    human_response = interrupt({
        "question": "Do you approve this diagnosis?",
        "equipment_id": equipment_id,
        "diagnostic_findings": diagnostic_findings,
        "manual_references": knowledge_summary,
        "retry_count": retry_count
    })

    approved = human_response.get("approved", False)
    feedback = human_response.get("feedback", "")

    if approved:
        return {
            "human_approved": True,
            "human_feedback": None,
            "messages": [AIMessage(content="HITL: Human engineer approved the diagnosis.")],
            "next_agent": "report_writer"
        }
    else:
        return {
            "human_approved": False,
            "human_feedback": feedback,
            "retry_count": retry_count + 1,
            "messages": [AIMessage(content=f"HITL: Human rejected diagnosis. Feedback: {feedback}")],
            "next_agent": "diagnostic"
        }