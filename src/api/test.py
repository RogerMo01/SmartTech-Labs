from agents.plan import *
from agents.task import *
from House import House
from llm.gemini import Gemini
from llm.prompts import *
import json

llm = Gemini()

conversation1 = [
    "Pedro dice: Oye Will-E",
    "Will-E dice: ¿En qué puedo asistirte?",
    "Pedro dice: Quiciera ver una película en casa",
    "Will-E dice: ¡Perfecto! Puedo recomendarte una película según tus gustos.",
    "Pedro dice: Me gustan las películas de ciencia ficción y las animaciones.",
    "Will-E dice: Entiendo. Voy a buscar algunas opciones y te las mostraré."
]
conversation2 = [
    "Pedro dice: Oye Will-E",
    "Will-E dice: ¿En qué puedo asistirte?",
    "Pedro dice: Estaba pensando en empezar a leer un nuevo libro.",
    "Will-E dice: ¡Genial! Puedo recomendarte algunos libros según tus intereses.",
    "Pedro dice: Me gusta la ciencia ficción y la fantasía.",
    "Will-E dice: Entiendo. Tengo algunas opciones interesantes que podrían interesarte.",
    "Pedro dice: Prefiero algo que sea parte de una serie.",
    "Will-E dice: Claro, puedo buscar algunas sagas populares dentro de esos géneros.",
    "Pedro dice: Eso sería perfecto, Will-E. Gracias.",
    "Will-E dice: No hay de qué, Pedro. Siempre estoy aquí para ayudarte.",
]


likes = {
    "comida": ["vegetariana", "sushi", "ensaladas"],
    "musica": ["música electrónica", "ambiental", "clásica"],
    "peliculas": ["documentales"]
}


instruction = human_likes_instruction_prompt(conversation2, likes)
resp = llm(instruction)

print(resp)
# print("Acción:", values[0])
# prompt = human_plan_generator_prompt(values[0])
# response = llm(prompt, True)
# print("Tarea:", response)