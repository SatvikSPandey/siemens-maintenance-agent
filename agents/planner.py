from langchain_ollama import ChatOllama
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AIMessage
import os
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, COHERE_LLM_MODEL, USE_OLLAMA

def get_cohere_key():
    try:
        import streamlit as st
        return st.secrets["COHERE_API_KEY"]
    except:
        return os.getenv("COHERE_API_KEY")


def planner_agent(state: dict) -> dict:
    equipment_id = state["equipment_id"]
    symptoms = state["symptoms"]

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