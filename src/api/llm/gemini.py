import os
from typing import Any
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import *
from llm.llm import LLM

class Gemini(LLM):
    def __init__(self) -> None:        
        # Load API KEY variable from .env file
        load_dotenv()
        key = os.getenv("API_KEY")
        genai.configure(api_key=key)

        self.model = genai.GenerativeModel('gemini-pro')


    def __call__(self, query: str, restrict=False) -> str:
        safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
        if restrict:
            response = self.model.generate_content(query, 
                generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                stop_sequences=['x'],
                max_output_tokens=50,
                temperature=1.0),
                safety_settings=safety_settings)
        else:
            response = self.model.generate_content(query, safety_settings=safety_settings)
        
        return response.text 
