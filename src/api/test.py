from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini
from llm.prompts import *
import json

llm = Gemini()
instruction = bot_need_plan_generator_prompt("alcanzame el movil")
resp = llm(instruction, 0.1)
print(resp)
# print("Acción:", values[0])
# prompt = human_plan_generator_prompt(values[0])
# response = llm(prompt, True)
# print("Tarea:", response)