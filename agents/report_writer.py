from langchain_ollama import ChatOllama
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AIMessage
import os
from tools.report_tools import generate_work_order
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, COHERE_LLM_MODEL, USE_OLLAMA


def get_cohere_key():
    try:
        import streamlit as st
        return st.secrets["COHERE_API_KEY"]
    except:
        return os.getenv("COHERE_API_KEY")


def report_writer_agent(state: dict) -> dict:
    equipment_id = state["equipment_id"]
    symptoms = state["symptoms"]
    diagnostic_findings = state.get("diagnostic_findings", "")
    knowledge_retrieved = state.get("knowledge_retrieved", [])
    maintenance_plan = state.get("maintenance_plan", "")

    knowledge_text = "\n".join([
        item["content"] for item in knowledge_retrieved
    ]) if knowledge_retrieved else "No manual references found"

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

    prompt = f"""You are a maintenance report writer.

Based on the following information, create a structured maintenance work order.

Equipment ID: {equipment_id}
Symptoms: {symptoms}
Diagnostic findings: {diagnostic_findings}
Manual references: {knowledge_text}
Investigation plan: {maintenance_plan}

Respond in this exact format:
DIAGNOSIS SUMMARY: [one sentence summary]
SEVERITY: [low/medium/high/critical]
ACTION PLAN: [numbered steps]
PARTS REQUIRED: [list parts needed]
ESTIMATED HOURS: [number only]
CONFIDENCE SCORE: [0.0 to 1.0]"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    def extract(label, multiline=False):
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith(label):
                if not multiline:
                    return line.replace(label, "").strip()
                result = []
                for j in range(i + 1, len(lines)):
                    if any(lines[j].startswith(l) for l in [
                        "DIAGNOSIS SUMMARY:", "SEVERITY:", "ACTION PLAN:",
                        "PARTS REQUIRED:", "ESTIMATED HOURS:", "CONFIDENCE SCORE:"
                    ]):
                        break
                    if lines[j].strip():
                        result.append(lines[j].strip())
                return " | ".join(result)
        return ""

    report_data = {
        "equipment_id": equipment_id,
        "symptoms": symptoms,
        "diagnosis": extract("DIAGNOSIS SUMMARY:"),
        "severity": extract("SEVERITY:"),
        "action_plan": extract("ACTION PLAN:", multiline=True),
        "parts_required": extract("PARTS REQUIRED:", multiline=True),
        "estimated_hours": extract("ESTIMATED HOURS:"),
        "confidence_score": extract("CONFIDENCE SCORE:"),
    }

    file_paths = generate_work_order(report_data)

    return {
        "final_report": {**report_data, **file_paths},
        "messages": [AIMessage(content=f"Report Writer: Work order generated at {file_paths['excel_path']}")],
        "next_agent": "end"
    }