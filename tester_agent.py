import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, HumanMessage
from utils.helpers import load_prompt

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini Flash model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load test case generation prompt template
TESTER_PROMPT_TEMPLATE = load_prompt(r"C:\one drive new\OneDrive\coding\AutoTestCaseGen\prompts\tester_prompt.txt")

def generate_test_cases(field: dict, review: str = "") -> tuple[str, str]:
    """Generate test cases, optionally incorporating feedback."""
    formatted_prompt = TESTER_PROMPT_TEMPLATE.format(
        FIELD_NAME=field.get("Field Name", ""),
        DATA_TYPE=field.get("Data Type", ""),
        REQUIRED=field.get("Required", ""),
        FORMAT=field.get("Format", ""),
        VALID_VALUES=field.get("Valid Values", ""),
        DESCRIPTION=field.get("Description", ""),
        REVIEW_FEEDBACK=review  # << pass this
    )
    response = model.generate_content(formatted_prompt)
    response_text = response.candidates[0].content.parts[0].text
    return formatted_prompt, response_text


def tester_agent_logic(state):
    field = state["field"]
    review = state.get("review", "")  # New
    iteration = state.get("iteration", 0) + 1

    prompt, test_cases = generate_test_cases(field, review)

    return {
        "messages": state.get("messages", []) + [
            HumanMessage(content=prompt),
            AIMessage(content=test_cases)
        ],
        "test_cases": test_cases,
        "field": field,
        "iteration": iteration
    }


tester_agent = RunnableLambda(tester_agent_logic)
