import os
from typing import Any
from dotenv import load_dotenv
import google.generativeai as genai
from llm.llm import LLM

class Gemini(LLM):
    def __init__(self) -> None:        
        # Load API KEY variable from .env file
        load_dotenv()
        key = os.getenv("API_KEY")
        genai.configure(api_key=key)

        self.model = genai.GenerativeModel('gemini-pro')


    def __call__(self, query: str, restrict=False) -> str:
        if restrict:
            response = self.model.generate_content(query, 
                generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                stop_sequences=['x'],
                max_output_tokens=50,
                temperature=0.8))
        else:
            response = self.model.generate_content(query)
        
        return response.text 
