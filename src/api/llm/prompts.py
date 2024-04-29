import simulation_data

def human_instruction_request_prompt():
    human_instruction = """
    Eres Alex, un agente operando en un entorno virtual compartido que representa una casa con varias divisiones y objetos específicos en cada una:

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

def plan_generator_prompt(intention: str):
    obj_actions = simulation_data.robot_obj_actions.copy()
    for i in range(len(obj_actions)):
        obj_actions[i] += " <objeto>"
    area_actions = simulation_data.robot_area_actions.copy()
    for i in range(len(area_actions)):
        area_actions[i] += " <area>"
    
    
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