# Agentic-AI-Test-Case-Generator


Agentic AI Test Case Generator

What I've created is an AI-driven, multi-agent system that automates test case generation from structured data dictionaries using [LangGraph](https://www.langchain.com/langgraph) and [LangChain](https://www.langchain.com/). Inspired by real-world QA workflows, this system coordinates intelligent agents (Tester, Senior Tester, Test Lead) to collaboratively generate, review, and refine test scenarios — with human-in-the-loop.


Features:

Multi-Agent Workflow: Simulates a QA pipeline with Tester, Senior Tester, and Test Lead agents.
Data Dictionary Ingestion: Parses structured field-level specs to seed test generation.
Iterative Refinement: Uses review feedback and conditional logic to improve test cases.
Memory-Driven State Machine: Maintains message history, iteration count, and decisions across agents.
Human-in-the-Loop Option: Prompts for clarification when data is ambiguous or incomplete.
JSON Output: Stores test cases and reviews for each field in a structured file.
Graph Visualization: Generates a Mermaid-based image of the agentic workflow.




Tech Stack:

- Python 3.10+
- [LangChain](https://python.langchain.com/)
- [LangGraph](https://www.langchain.com/langgraph)
- `pandas`, `re`, `json`, `IPython.display`, etc.

---

How It Works:

1. Read the Data Dictionary: Each field (e.g., name, type, constraints) is read from a CSV.
2. Kick off the Workflow: `test_lead_agent` checks if the field is ready or needs clarification.
3. Generate Test Cases: `tester_agent` creates test scenarios based on field characteristics.
4. Review and Score: `senior_tester_agent` evaluates and scores test cases (e.g., 85%).
5. **Iterate or Finalize**: If score ≥ 90% or 3 iterations are reached, the output is saved. Else, the cycle continues.

---

Sample Graph Visualization

->A Mermaid-generated visual of the agent flow is saved.

Use Cases:

 Enterprise QA automation tools
 AI-assisted testing pipelines
 Auto-documentation for specs
 Prompt engineering test harness

Project Structure:

agentictest/
├── main.py # Entry script to run the full test case generation loop
├── graphs/
│ └── main_graph.py # Defines the LangGraph workflow with all agent transitions
├── agents/
│ ├── test_lead_agent.py # Clarifies data dictionary entries
│ ├── tester_agent.py # Generates test cases based on the field metadata
│ └── senior_tester_agent.py # Reviews and scores the test cases
├── data/
│ └── data_dictionary.csv # Input CSV file containing field metadata
├── output/
│ └── final_test_cases.json # Generated output of test cases and reviews
└── graph_output.png # Mermaid visualization of the graph



Author

Akshit Singh

