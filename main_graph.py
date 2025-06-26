# graphs/main_graph.py
import sys
import os
import re
from typing import TypedDict, List, Dict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from IPython.display import Image
import pathlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.test_lead_agent import test_lead_agent
from agents.tester_agent import tester_agent
from agents.senior_tester_agent import senior_tester_agent

# Define state
class GraphState(TypedDict):
    messages: List
    data_dictionary: str
    test_cases: str
    review: str
    field: Dict
    iteration: int
    lead_review_complete: bool

# Logic to check if data dictionary is ready
def check_data_dictionary_status(state: GraphState) -> str:
    last_message = state["messages"][-1].content.lower() if state["messages"] else ""
    if "data dictionary is complete" in last_message:
        return "ready"
    return "needs_more_info"

# Logic to check alignment score
def should_refine_test_cases(state: GraphState) -> str:
    review_text = state.get("review", "")
    iteration = state.get("iteration", 0)

    match = re.search(r'(\d+)%', review_text)
    score = int(match.group(1)) if match else 100

    return "exit" if score >= 90 or iteration >= 3 else "refine"

# Build graph
memory = MemorySaver()
graph_builder = StateGraph(GraphState)

graph_builder.add_node("test_lead", test_lead_agent)
graph_builder.add_node("tester", tester_agent)
graph_builder.add_node("senior_tester", senior_tester_agent)

graph_builder.set_entry_point("test_lead")
graph_builder.add_edge("tester", "senior_tester")

# Loops
graph_builder.add_conditional_edges("test_lead", check_data_dictionary_status, {
    "ready": "tester",
    "needs_more_info": "test_lead"
})
graph_builder.add_conditional_edges("senior_tester", should_refine_test_cases, {
    "refine": "tester",
    "exit": "__end__"
})

# Compile with memory checkpointing
graph = graph_builder.compile(checkpointer=memory) 

try:
    image_data = graph.get_graph().draw_mermaid_png()
    image_path = pathlib.Path("graph_output.png")
    image_path.write_bytes(image_data)  # Save image to file
    print(f"Graph image saved to: {image_path.resolve()}")
except Exception as e:
    print(f"Error generating image: {e}")