from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages


class MaintenanceState(TypedDict):
    equipment_id: str
    symptoms: str
    equipment_history: Optional[list]
    diagnostic_findings: Optional[str]
    knowledge_retrieved: Optional[list]
    maintenance_plan: Optional[str]
    final_report: Optional[dict]
    human_approved: Optional[bool]
    human_feedback: Optional[str]
    next_agent: Optional[str]
    retry_count: Optional[int]
    error: Optional[str]
    messages: Annotated[list, add_messages]


def get_initial_state(equipment_id: str, symptoms: str) -> MaintenanceState:
    return MaintenanceState(
        equipment_id=equipment_id,
        symptoms=symptoms,
        equipment_history=None,
        diagnostic_findings=None,
        knowledge_retrieved=None,
        maintenance_plan=None,
        final_report=None,
        human_approved=None,
        human_feedback=None,
        next_agent="planner",
        retry_count=0,
        error=None,
        messages=[],
    )