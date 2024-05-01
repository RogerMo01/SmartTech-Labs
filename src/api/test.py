from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini
from llm.prompts import generate_human_intention, human_instruction_request_prompt

# start = "2024-01-24T18:00:00.000000"
# format = "%Y-%m-%dT%H:%M:%S.%f"
# hora = datetime.strptime(start, format)

# en = 'bajo'
# ha = 'máximo'
# ve = 'alto'
# hi = 'máximo'
# entret = 'alto'

# prompt = generate_human_intention(en, ha, ve, hi, entret, hora.time())
# llm = Gemini()
# response = llm(prompt, True)
# print(response)

area = 'sala de estar'
prompt = human_instruction_request_prompt(area)
llm = Gemini()
response = llm(prompt, True)
print(response)