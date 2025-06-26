from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from utils.helpers import load_prompt
import google.generativeai as genai
import os

# Load Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load prompt
CRITIQUE_PROMPT = load_prompt(r"C:\one drive new\OneDrive\coding\AutoTestCaseGen\prompts\senior_tester_prompt.txt")

def get_senior_tester_messages(state):
    combined_input = f"""You will be reviewing test cases based on the data dictionary.

--- DATA DICTIONARY ---
{state["data_dictionary"]}

--- TEST CASES ---
{state["test_cases"]}

Please critique the test cases based on alignment with the field-level requirements.
"""
    return [
        SystemMessage(content=CRITIQUE_PROMPT),
        HumanMessage(content=combined_input)
    ]

def senior_tester_agent_logic(state):
    messages = get_senior_tester_messages(state)
    full_text = "\n".join([m.content for m in messages])
    response = model.generate_content(full_text)
    response_text = response.candidates[0].content.parts[0].text

    return {
        "messages": state.get("messages", []) + [AIMessage(content=response.text)],
        "review": response_text,
        "data_dictionary": state["data_dictionary"],
        "test_cases": state["test_cases"],
        "field": state["field"],
        "iteration": state.get("iteration", 0)
    }

senior_tester_agent = RunnableLambda(senior_tester_agent_logic)
