from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini
from llm.prompts import *
import json

llm = Gemini()
instruction = generate_action_values('Hambre', 26)
values = llm(instruction, True)
values = json.loads(values)
print("Acción:", values[0])
prompt = human_plan_generator_prompt(values[0])
response = llm(prompt, True)
print("Tarea:", response)