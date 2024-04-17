import os
from typing import Any
from dotenv import load_dotenv
import google.generativeai as genai
from api.llm import LLM

class Gemini(LLM):
    def __init__(self) -> None:        
        # Load API KEY variable from .env file
        load_dotenv()
        key = os.getenv("API_KEY")
        genai.configure(api_key=key)

        self.model = genai.GenerativeModel('gemini-pro')


    def __call__(self, query: str) -> str:
        response = self.model.generate_content(query)
        return response.text