from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini

llm = Gemini()
response = llm(prompt, True)
print(response)
x = json.loads(response)