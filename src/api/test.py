from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini
from llm.prompts import generate_action_values

prompt = generate_action_values('Dormir', 23)
llm = Gemini()
response = llm(prompt, True)
print(response)