import os
import json
import pandas as pd
from langchain_core.messages import HumanMessage
from graphs.main_graph import graph
from langgraph.checkpoint.memory import MemorySaver

# Load CSV data dictionary
df = pd.read_csv(r"C:\one drive new\OneDrive\coding\AutoTestCaseGen\data\data_dictionary.csv")
data_dict = df.to_dict(orient="records")

# Setup memory and session config
memory = MemorySaver()
config = {"configurable": {"thread_id": "session-001"}}

final_outputs = []

print("=== LangGraph Test Case Generator ===")

for i, field in enumerate(data_dict):
    print(f"\n=== FIELD {i+1}/{len(data_dict)}: {field['Field Name']} ===")

    state = {
        "messages": [],
        "data_dictionary": json.dumps(field, indent=2),
        "test_cases": "",
        "review": "",
        "field": field,
        "iteration": 0,
        "lead_review_complete": False,
    }

    while True:
        should_continue = True

        for step in graph.stream(state, config=config, stream_mode="updates"):
            for node_name, result in step.items():
                print(f"\n Agent: {node_name}")
                messages = result.get("messages", [])
                if messages:
                    print("--", messages[-1].content.strip())

                state = result  # Update working state

                # Proceed if test_cases are generated
                if result.get("test_cases"):
                    should_continue = True
                    break

                # Else handle clarification only from test_lead
                if node_name == "test_lead":
                    user_input = input("\nRespond to Test Lead (or type 'done' if clarified):\n")
                    if user_input.strip().lower() == "done":
                        state["messages"].append(HumanMessage(content="The data dictionary is complete."))
                    else:
                        state["messages"].append(HumanMessage(content=user_input))
                    should_continue = False
                    break

        if should_continue and state.get("test_cases"):
            break  # Exit loop if test cases are ready

    # Save results
    final_outputs.append({
        "field": field["Field Name"],
        "test_cases": state.get("test_cases", ""),
        "review": state.get("review", "")
    })

# Save output
os.makedirs("output", exist_ok=True)
with open("output/final_test_cases.json", "w") as f:
    json.dump(final_outputs, f, indent=2)

print("\nAll fields processed. Results saved to 'output/final_test_cases.json'") 