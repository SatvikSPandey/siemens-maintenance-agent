import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from langgraph.types import Command
from graph.graph_builder import build_graph
from graph.state import get_initial_state

st.set_page_config(page_title="Industrial Equipment Maintenance Agent", page_icon="🔧")
st.title("🔧 Industrial Equipment Maintenance Agent")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "stage" not in st.session_state:
    st.session_state.stage = "input"

if "interrupt_data" not in st.session_state:
    st.session_state.interrupt_data = None

if "final_report" not in st.session_state:
    st.session_state.final_report = None


def run_until_interrupt(equipment_id, symptoms):
    state = get_initial_state(equipment_id, symptoms)
    thread_id = f"run-{equipment_id}"
    st.session_state.thread_id = thread_id
    config = {"configurable": {"thread_id": thread_id}}

    for event in st.session_state.graph.stream(state, config=config):
        for node_name, node_output in event.items():
            if node_name == "__interrupt__":
                st.session_state.interrupt_data = node_output
                st.session_state.stage = "review"
                return


def resume_graph(approved, feedback=""):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    human_response = Command(resume={"approved": approved, "feedback": feedback})

    for event in st.session_state.graph.stream(human_response, config=config):
        for node_name, node_output in event.items():
            if "final_report" in node_output:
                st.session_state.final_report = node_output["final_report"]
                st.session_state.stage = "complete"
            elif node_name == "__interrupt__":
                st.session_state.interrupt_data = node_output
                st.session_state.stage = "review"


if st.session_state.stage == "input":
    st.subheader("Enter Equipment Details")
    equipment_id = st.text_input("Equipment ID", placeholder="e.g. PUMP-001")
    symptoms = st.text_area("Describe the fault or symptoms", placeholder="e.g. Unusual vibration and high temperature since Monday")

    if st.button("Run Diagnosis"):
        if equipment_id and symptoms:
            with st.spinner("Running multi-agent diagnosis..."):
                run_until_interrupt(equipment_id, symptoms)
            st.rerun()
        else:
            st.warning("Please enter both Equipment ID and symptoms.")


elif st.session_state.stage == "review":
    st.subheader("AI Diagnosis — Please Review")

    interrupt_data = st.session_state.interrupt_data
    if interrupt_data:
        data = interrupt_data[0].value if hasattr(interrupt_data[0], 'value') else {}
        st.markdown("**Equipment ID:**")
        st.write(data.get("equipment_id", ""))
        st.markdown("**Diagnostic Findings:**")
        st.write(data.get("diagnostic_findings", ""))
        st.markdown("**Manual References:**")
        st.write(data.get("manual_references", ""))

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve Diagnosis", type="primary"):
            with st.spinner("Generating work order..."):
                resume_graph(approved=True)
            st.rerun()

    with col2:
        feedback = st.text_area("Rejection reason (required if rejecting)")
        if st.button("❌ Reject and Retry"):
            if feedback:
                with st.spinner("Sending feedback to diagnostic agent..."):
                    resume_graph(approved=False, feedback=feedback)
                st.rerun()
            else:
                st.warning("Please provide a reason for rejection.")


elif st.session_state.stage == "complete":
    st.success("Work order generated successfully.")
    report = st.session_state.final_report

    st.subheader("Final Work Order")
    st.markdown(f"**Equipment ID:** {report.get('equipment_id')}")
    st.markdown(f"**Diagnosis:** {report.get('diagnosis')}")
    st.markdown(f"**Severity:** {report.get('severity')}")
    st.markdown(f"**Action Plan:** {report.get('action_plan')}")
    st.markdown(f"**Parts Required:** {report.get('parts_required')}")
    st.markdown(f"**Estimated Hours:** {report.get('estimated_hours')}")
    st.markdown(f"**Confidence Score:** {report.get('confidence_score')}")

    st.divider()
    st.markdown(f"📊 Excel report saved to: `{report.get('excel_path')}`")
    st.markdown(f"📄 JSON report saved to: `{report.get('json_path')}`")

    if st.button("Start New Diagnosis"):
        for key in ["thread_id", "stage", "interrupt_data", "final_report"]:
            del st.session_state[key]
        st.rerun()