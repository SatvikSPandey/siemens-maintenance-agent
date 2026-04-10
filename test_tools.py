from langgraph.types import Command
from graph.graph_builder import build_graph
from graph.state import get_initial_state

graph = build_graph()

state = get_initial_state(
    "PUMP-001",
    "Unusual vibration and high temperature since Monday"
)

config = {"configurable": {"thread_id": "test-run-001"}}

print("--- Running graph until interrupt ---")
for event in graph.stream(state, config=config):
    for node_name, node_output in event.items():
        print(f"{node_name} ran")

print("\n--- Simulating human approval ---")
human_response = Command(resume={"approved": True, "feedback": ""})

for event in graph.stream(human_response, config=config):
    for node_name, node_output in event.items():
        print(f"{node_name} ran")
        if "final_report" in node_output:
            print(f"\nFinal report generated:")
            print(f"Diagnosis: {node_output['final_report'].get('diagnosis')}")
            print(f"Severity: {node_output['final_report'].get('severity')}")
            print(f"Excel: {node_output['final_report'].get('excel_path')}")