import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load from .env file
load_dotenv()

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    genai.configure(api_key=api_key)

    # Use Gemini 1.5 Flash model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    return model

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

