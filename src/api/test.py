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

conversation3 = [
    "Pedro dice: Oye Will-E, recomiendame una cacion", 
    "Will-E dice: Por supuesto Pedro, ¿qué género te gustaría?",
    "Pedro dice: ¿Quizás algo de rock?",
    "Will-E dice: Tengo una lista de excelentes canciones de rock, ¿tienes algún artista o banda en particular que prefieras?",
    "Pedro dice: \"Creo que me gustaría algo de Green Day.",
    "Will-E dice: Vale, tengo algunas canciones geniales de Green Day en mi lista. ¿Te gustaría que te pusiera una ahora mismo?", 
    "Pedro dice: Sí, por favor", 
    "Will-E dice: Claro Pedro, aquí tienes una canción de Green Day. Disfrútala!",
    "Pedro dice: Gracias Will-E!"
]

conversation4 = [
    "Pedro dice: Oye Will-E, recomiendame una cacion", 
    "Will-E dice: ¿Qué género musical te gusta más, Pedro?",
    "Pedro dice: Rock",
    "Will-E dice: ¿Qué tal AC/DC, Guns N' Roses o Metallica?",
    "Pedro dice: Me gusta AC/DC y Guns N' Roses. Gracias Will-E",
    "Will-E dice: De nada Pedro. Disfruta la música."
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