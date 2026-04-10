import os
from langchain_ollama import ChatOllama
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AIMessage
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, COHERE_LLM_MODEL, USE_OLLAMA


def get_cohere_key():
    try:
        import streamlit as st
        return st.secrets["COHERE_API_KEY"]
    except:
        return os.getenv("COHERE_API_KEY")


def diagnostic_agent(state: dict) -> dict:
    equipment_id = state["equipment_id"]
    symptoms = state["symptoms"]
    history = state.get("equipment_history", [])
    plan = state.get("maintenance_plan", "")
    human_feedback = state.get("human_feedback", None)
    retry_count = state.get("retry_count", 0)

    history_text = "\n".join([
        f"- {r['date']} | {r['event_type']} | {r['description']}"
        for r in history
    ]) if history else "No history available"

    feedback_section = ""
    if human_feedback:
        feedback_section = f"""
Previous diagnosis was rejected by human engineer.
Their feedback: {human_feedback}
Please reconsider your diagnosis based on this feedback.
"""

    if USE_OLLAMA:
        llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.1
        )
    else:
        llm = ChatCohere(
            cohere_api_key=get_cohere_key(),
            model=COHERE_LLM_MODEL,
            temperature=0.1
        )

    prompt = f"""You are an expert industrial equipment diagnostic engineer.

Equipment ID: {equipment_id}
Reported symptoms: {symptoms}

Maintenance history:
{history_text}

Investigation plan:
{plan}

{feedback_section}

Provide your diagnosis in this exact format:
PROBABLE CAUSE: [what is most likely wrong]
SEVERITY: [low/medium/high/critical]
CONFIDENCE: [0.0 to 1.0]
REASONING: [explain why you reached this conclusion]
RECOMMENDED ACTION: [what should be done immediately]"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "diagnostic_findings": response.content,
        "messages": [AIMessage(content=f"Diagnostic: {response.content}")],
        "retry_count": retry_count,
        "next_agent": "knowledge"
    }