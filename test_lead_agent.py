from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from utils.helpers import load_prompt
import google.generativeai as genai
import os

# Load Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load prompt from file
TEST_LEAD_PROMPT = load_prompt(r"C:\one drive new\OneDrive\coding\AutoTestCaseGen\prompts\test_lead_prompt.txt")

def get_test_lead_messages(state):
    data_dictionary_str = state.get("data_dictionary", "")
    messages = state.get("messages", [])
    
    return [
        SystemMessage(content=TEST_LEAD_PROMPT),
        HumanMessage(content=f"Please review the following data dictionary:\n\n{data_dictionary_str}")
    ] + messages

def test_lead_agent_logic(state):
    messages = get_test_lead_messages(state)
    prompt_text = "\n".join([msg.content for msg in messages if hasattr(msg, 'content')])
    response = model.generate_content(prompt_text)
    response_text = response.candidates[0].content.parts[0].text
    return {
        "messages": state.get("messages", []) + [AIMessage(content=response_text)],
        "data_dictionary": state["data_dictionary"]
    }


test_lead_agent = RunnableLambda(test_lead_agent_logic)

# Optional wrapper
def review_data_dictionary(state):
    return test_lead_agent.invoke(state)
