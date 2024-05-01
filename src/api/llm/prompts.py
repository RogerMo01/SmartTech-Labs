import simulation_data

#################### Pedro prompts #######################
def human_instruction_request_prompt():
    human_instruction = """
    Eres Pedro, un agente operando en un entorno virtual compartido que representa una casa con varias divisiones y objetos específicos en cada una:

    Sala:
    - Sofá
    - TV
    - Maceta con planta
    - Mesa de comedor

    Cuarto:
    - Armario
    - Maceta con planta
    - Cama
    - Mesa de noche
        - libro
        - movil 

    Baño:
    - Bañadera
    - Lavamanos
    - Inodoro

    Cocina:
    - Meseta en forma de isla
    - Maceta con planta
    - Friega platos
    - Cafetera para preparar cafe

    Además, en dicho entorno se encuentran tus chancletas de andar por casa.

    Utiliza esta información para formular una única petición al agente Xero que incluya solo una acción a realizar y que refleje la tarea que un agente real podría realizar por ti en un entorno doméstico.

    """

    return human_instruction

def instruction_interpreter_prompt(request: str, available_actions: list):
    robot_instruction = f"""
    Eres Xero, un agente operando en un entorno virtual compartido. 
    
    Tu misión es cumplir las peticiones de Alex, un agente humano. Para ello, debes reconocer dentro de una lista de posibles acciones que tienes definidas, 
    a cuáles se hace referencia implícita o explícitamente en la petición descrita en lenguaje natural realizada 
    por el humano. Ten en cuenta que en dicha petición puede haber más de una acción a realizar. 
    
    Si la elección de la acción es ambigua ya sea porque no la tienes definida o porque haya mas de una acción a realizar y una de ellas no la tengas definida, responde lo siguiente: Lo siento, no entiendo lo que me pides :(
    
    En caso de identificar la acción, responde con el siguiente formato JSON:
    {{
        acción: nombre_de_la_acción, tal y como aparece en la lista,
        objeto: nombre del objeto sobre el cual se quiere realizar la acción
    }}
    
    acciones = {available_actions}

    peticion = "{request}"
    
    """
    return robot_instruction

def generate_human_intention(energy, hungry, bladder, hygiene, enjoy, time):
    pass

###################### Will-E prompts ########################
def plan_generator_prompt(intention: str):
    obj_actions, area_actions = get_actions()
    
    plan_instruction = f"""
Eres un robot llamado Will-E, destinado a asistir y ayudar a Pedro. Ambos conviven en una casa. Todas las tareas que
cumples como robot se desarrollan dentro de la casa.

A continuación se muestra una lista de los objetos que hay en la casa:
{make_list(simulation_data.objects_names)}
Pedro

En la casa también está Pedro, que es la persona a la que estás destinado a ayudar.

A continuación se muestra una lista de areas de la casa:
{make_list(simulation_data.areas)}

A continuación se muestra una lista de tareas que se utilizan para elaborar un plan:
{make_list(obj_actions)}
{make_list(area_actions)}

Tu objetivo es, a partir de una intención (que se encuentra debajo donde dice Intención) en lenguaje natural,
formar un plan, haciendo una lista de tareas de la lista anterior de posibles tareas. 
Para poner una tarea en la lista se debe completar la sección <objeto> o <area>, con un objeto o area de la lista de objetos
y de areas de la casa, listas dadas anteriormente. Notar que para usar un objeto hay q caminar hasta él.

Por ejemplo: 
para la intención (Encender el televisor), la lista de tareas de salida debe ser
["CAMINAR_HASTA tv", "ENCENDER tv"]
para la intención (Limpiar el dormitorio), la lista de tareas de salida debe ser
["CAMINAR_HASTA dormitorio", LIMPIAR dormitorio]


Ahora si, debes procesar la siguiente intención
Intención: {intention}
"""

    return plan_instruction


def make_list(arr: list):
    response = ""
    for i in arr:
        response += i
        response += "\n"

    return response


def validate_instruction_prompt(order: str):
    obj_actions, area_actions = get_actions()
    
    instruction = f"""
Eres un robot llamado Will-E, destinado a asistir y ayudar a Pedro. Ambos conviven en una casa. Todas las tareas que
cumples como robot se desarrollan dentro de la casa.

A continuación se muestra una lista de los objetos que hay en la casa:
{make_list(simulation_data.objects_names)}
Pedro

En la casa también está Pedro, que es la persona a la que estás destinado a ayudar.

A continuación se muestra una lista de areas de la casa:
{make_list(simulation_data.areas)}

A continuación se muestra una lista de acciones que puedes hacer:
{make_list(obj_actions)}
{make_list(area_actions)}

Tu objetivo es determinar dada la lista de posibles acciones a realizar sobre los objetos que hay en la casa y 
la lista de acciones a realizar sobre las areas de la casa, si la orden (que se encuentra debajo donde dice Orden) 
en lenguaje natural, entra en el espectro de las acciones que tu puedes realizar sobre los objetos.
Debes poder interpretar la orden, como algo que se pueda realizar combinando acciones de la lista

Debes responder con la palabra (No) en caso de que no identifiques la accion. De lo contrario escribe la orden 
de forma explicita, utilizando su verbo en infinitivo, y con los suficientes datos para que se entienda la intención.

Debes asegurarte que la orden se pueda cumplir utilizando estrictamente las acciones de la lista de acciones mencionada anteriormente.

Debes asegurarte que todo objeto que se utilice en la orden, esté en la lista de objetos dada anteriormente.
Si el objeto no aparece, debes responder: No


Por ejemplo:
para la orden (Pedro dice: Oye Will-E, friega los platos) tu respuesta debe ser: No
para la orden (Pedro dice: Oye Will-E, por favor riega las plantas) tu respuesta debe ser: Regar las plantas
para la orden (Pedro dice: Oye Will-E, ve hasta la sala y pon el canal 123) tu respuesta debe ser: Encender el televisor
para la orden (Pedro dice: Oye Will-E, prepara una taza de cafe) tu respuesta debe ser: No 
porque no hay cafetera en la lista de objetos
para la orden (Pedro dice: Oye Will-E, ve a la cocina) tu respuesta debe ser: Ir a la cocina 
para la orden (Pedro dice: Oye Will-E, siéntate en el sofá) tu respuesta debe ser: No
para la orden (Pedro dice: Oye Will-E, alcánzame un vaso de agua) tu respuesta debe ser: No
porque el vaso no está en la lista de objetos
para la orden (Pedro dice: Oye Will-E, alcánzame las chancletas) tu respuesta debe ser: Llevar las chanclas a Pedro

Ahora si, analiza la siguiente orden dada por Pedro:
Orden: {order}
"""
    return instruction

def generate_action_values(need:str, level:int):  #accion, tiempo que se le va a dedicar, cuanto sube la necesidad.
    prompt =f"""
        Eres un humano llamado Pedro, Pedro tiene una necesidad la cual quiere satisfacer teniendo en cuenta los objetos que hay en su casa.
        Los objetos que hay en la casa de Pedro con los cuales puede satisfacer cierta necesidad, según corresponda, son los siguientes:
        {make_list(simulation_data.objects_names)}. 
        Satisfacer cada necesidad debe demorar un tiempo, el cual quiero que proveas, y además, la necesidad tiene un
        nivel {level} del 1 al 100, siendo el 1 mínimo y el 100 máximo, quiero que me digas también, asumiendo que la necesidad está en un nivel inferior a 20, cuánto sube
        esta después de realizar la acción que elija Pedro, siempre teniendo en cuenta que {level} más lo que suba, no puede ser mayor que 100

        Por ejemplo:
        Para una necesidad Vejiga, una posible salida es:
        {
            {     'acción': 'Ir al inodoro',
                'tiempo_en_segundos': '300',
                'cantidad_incremento': '50'
            }
        } 
        Para una necesidad Hambre, una posible salida es:
        {
            {
                'acción': 'Comer un bocadillo',
                'tiempo_en_segundos': '240',
                'cantidad_incremento': '35'
            }
        }
        Para una necesidad Dormir, una posible salida es:
        {
            {    'acción': 'Echarse una siesta',
                'tiempo_en_segundos': '3600',
                'cantidad_incremento': '50'
            }
        }
        Para una necesidad Dormir, otra posible salida es:
        {
            {
                'acción': 'Acostarse a dormir',
                'tiempo_en_segundos': '28880',
                'cantidad_incremento': '80'
            }
        }

    """
    return prompt


def get_actions():
    obj_actions = simulation_data.robot_obj_actions.copy()
    for i in range(len(obj_actions)):
        obj_actions[i] += " <objeto>"
    area_actions = simulation_data.robot_area_actions.copy()
    for i in range(len(area_actions)):
        area_actions[i] += " <area>"

    return obj_actions, area_actions