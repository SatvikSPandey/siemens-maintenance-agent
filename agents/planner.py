from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from config import OLLAMA_MODEL, OLLAMA_BASE_URL


def planner_agent(state: dict) -> dict:
    equipment_id = state["equipment_id"]
    symptoms = state["symptoms"]

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1
    )

    prompt = f"""You are a maintenance planning expert.

Equipment ID: {equipment_id}
Reported symptoms: {symptoms}

Create a brief investigation plan with:
1. What data to collect
2. What to diagnose
3. What manuals to check

Keep it concise and practical."""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "maintenance_plan": response.content,
        "messages": [AIMessage(content=f"Planner: {response.content}")],
        "next_agent": "data_retrieval"
    }