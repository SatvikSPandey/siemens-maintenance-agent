from langchain_core.messages import AIMessage
from tools.equipment_tools import get_equipment_history


def data_retrieval_agent(state: dict) -> dict:
    equipment_id = state["equipment_id"]

    history = get_equipment_history(equipment_id)

    summary = f"Found {len(history)} maintenance records for {equipment_id}."

    return {
        "equipment_history": history,
        "messages": [AIMessage(content=f"Data Retrieval: {summary}")],
        "next_agent": "diagnostic"
    }