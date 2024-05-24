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

# class Sentence:
#     def __init__(self, speaker: str, message: str):
#         self.speaker = speaker
#         self.message = message

#     def __str__(self) -> str:
#         return f"{self.speaker} dice: {self.message}"
    
# conversations = [Sentence("Pedro", "Que puedo hacer para la cena?"), 
#                  Sentence("Will-E", "que te apetece para la cena?"),
#                  Sentence("Pedro", "quizás comida mexicana"),
#                  Sentence("Will-E", "tienes algun plato favorito?"),
#                  Sentence("Pedro", "No, sugiereme tu algo")
#                  ]

# conversations = [Sentence]
# prompt = f"""
# Eres Will-E, un robot asistente de compañía, y vives en una casa acompañando a Pedro.
# En este momento se encuentran en una conversación, a continuación se muestra la conversación.

# Conversación:
# {make_list([str(sentence) for sentence in conversations])}

# Ten en cuenta que puedes sugerir recetas.
# Es tu turno, puedes responderle algo, o simplemente terminar la conversación.
# Responde solo lo necesario.
# Sé lo más preciso y objetivo en tu respuesta.
# La conversación debe ser corta.

# Si decides responder, sustituye <out> con la respuesta de Will-E a Pedro en string con (")
# Si decides terminar la conversación, sustituye <out> con el string "END"
# Si entiendes que te pide una receta, sustituye <receta> con el string "SI", sino con "NO"

# {{
#     "response": <out>,
#     "recipe": <receta>
# }}

# tu salida debe ser este json
# """

conversations5 = [
    "Pedro: ¿Qué puedo hacer para la cena?",
    "Will-E: Bueno, podrías cenar unos deliciosos tacos al pastor.",
    "Pedro: ¡Suena genial! ¿Cómo se hacen?",
    "Will-E: Tradicionalmente, se marinan trozos de carne de cerdo con una mezcla de especias y achiote, luego se asan en un trompo vertical y se sirven en tortillas de maíz con cebolla, piña y cilantro.",
    "Pedro: Wow, suena delicioso! Pero ¿qué más podemos agregar?",
    "Will-E: Podemos acompañarlos con guacamole fresco, salsa picante y frijoles refritos.",
    "Pedro: ¡Perfecto! ¡Vamos a preparar esos tacos al pastor!",
    "Will-E: ¿Alguna vez has probado un auténtico curry tailandés?",
    "Pedro: No, nunca la he probado.",
    "Will-E: Es un plato aromático y sabroso que combina carne o mariscos con leche de coco, pasta de curry y una variedad de hierbas y especias."
]

# prompt = human_culinary_styles_likes_instruction_prompt(conversations5, simulation_data.culinary_styles)
# resp = llm(prompt)
# print(resp)

uno = datetime(year=2021, month=2, day=2, hour=14, minute=12, second=0)
dos = datetime(year=2028, month=6, day=4, hour=14, minute=12, second=0)
print(uno.strftime('%H:%M:%S'))
print(dos.strftime('%H:%M:%S'))
print(uno.strftime('%H:%M:%S') == dos.strftime('%H:%M:%S'))

hours = list(range(8, 24)) + list(range(0, 8))
for hour in hours:
    print(hour)
# print("Acción:", values[0])
# prompt = human_plan_generator_prompt(values[0])
# response = llm(prompt, True)
# print("Tarea:", response)