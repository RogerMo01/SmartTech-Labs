from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini
from llm.prompts import generate_action_values, validate_instruction_prompt
import json

prompt = generate_action_values('Energía',25)
llm = Gemini()
response = llm(prompt, True)
print(response)
x = json.loads(response)