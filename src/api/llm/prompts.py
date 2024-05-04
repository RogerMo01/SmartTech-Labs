import simulation_data

#################### Pedro prompts #######################
def human_instruction_request_prompt(area):
    human_instruction = f"""
    Eres Pedro, un agente operando en un entorno virtual compartido, dicho entorno es una casa con varias áreas de estar y objetos con los que interactuar:

    A continuación se muestra una lista de los objetos que hay en la casa:
    {make_list(simulation_data.objects_names)}
    Will-E

    En la casa también está Will-E, que es el robot asistente destinado a ayudarte.

    A continuación se muestra una lista de áreas de la casa:
    {make_list(simulation_data.areas)}

    Actualmente te encuentras en la siguiente habitación: {area}

    A continuación se muestra una lista de posibles acciones que el robot puede realizar sobre los objetos y las áreas de la casa:
    {make_list(simulation_data.robot_obj_actions)}
    {make_list(simulation_data.robot_area_actions)}

    Utiliza esta información para formular una única petición al agente Will-E.
    Esta petición debe estar formada por una de las acciones de la lista de posibles acciones a realizar sobre los objetos y un objeto de la lista de objetos, ó 
    por una de las acciones de la lista de posibles acciones a realizar sobre las áreas de la casa y un área de la lista de áreas de la casa. 
    

    Por ejemplo: 
    Oye Will-E, ven hacia acá.
    Oye Will-E, por favor riega las plantas.
    Oye Will-E, recoge las chancletas y llevalas hasta el dormitorio.
    Oye Will-E, enciende el televisor para ver mi programa favorito.
    Oye Will-E, tráeme el móvil, por favor.
    Oye Will-E, apaga el tv.

    Ten en cuenta que dicha petición tiene que reflejar una tarea que un robot real realizaría por ti en un entorno doméstico.

    Devuelve esta petición escrita en lenguaje natural siguiedo el siguiente formato:
    Oye Will-E, <petición>
    """

    return human_instruction


def human_instruction_request_for_need_prompt(need):
    human_instruction = f"""
    Eres Pedro, un agente operando en un entorno virtual compartido, dicho entorno es una casa con varias áreas de estar y objetos con los que interactuar:

    A continuación se muestra una lista de los objetos que hay en la casa:
    {make_list(simulation_data.objects_names)}
    Will-E

    En la casa también está Will-E, que es el robot asistente destinado a ayudarte.

    A continuación se muestra una lista de posibles acciones que el robot puede realizar sobre los objetos y las áreas de la casa, además de algunas acciones especiales para satisfacer al humano:
    {make_list(simulation_data.robot_obj_actions)}
    {make_list(simulation_data.robot_area_actions)}
    {make_list(simulation_data.robot_need_actions)}

    Ahora mismo, quieres satisfacer la necesidad {need}, y para ello tienes que formular una única petición al agente Will-E.
    Esta petición debe estar formada por una de las acciones de la lista de posibles acciones a realizar, estas acciones puede que impliquen el uso
    de los objetos anteriores o no , tambien puden ser por una de las acciones de la lista de posibles acciones a realizar sobre las áreas de la casa y un área de la lista de áreas de la casa. 
    

    Por ejemplo:
    Si la necesidad es Entretenimiento posibles salidas serían:  
    Oye Will-E, reproduce música.
    Oye Will-E, pon una buena canción.
    Oye Will-E, cuéntame un chiste.

    Si la necesidad es Higiene posibles salidas serían:
    Oye Will-E, limpia la sala de estar.
    Oye Will-E, limpia el baño.

    

    Ten en cuenta que dicha petición tiene que reflejar una tarea que un robot real realizaría por ti en un entorno doméstico.

    Devuelve esta petición escrita en lenguaje natural siguiedo el siguiente formato:
    Oye Will-E, <petición>
    """

    return human_instruction

def generate_action_values(need:str, level:int):  #acción, cuanto sube la necesidad.
    prompt =f"""
Eres un humano llamado Pedro y tienes una necesidad que quieres satisfacer(dicha necesidad se necuentra más abajo donde dice Necesidad).

La necesidad tiene un valor asociado que representa la saciedad de la misma, en este caso es: {level}, la cual está representada por un valor del 1 al 100, 
siendo 1 el mínimo y 100 el máximo.

Tu objetivo es devolver a cuanto asciende la saciedad de la misma luego de realizar una acción para satisfacerla.

Por ejemplo:
Para una necesidad Vejiga, una posible salida es:
["Ir al inodoro", 50]

Para una necesidad Vejiga, otra posible salida es:
["Ir al baño", 45] 

Para una necesidad Hambre, una posible salida es:
["Comer un bocadillo", 35]    

Para una necesidad Energía, una posible salida es:
["Dormir una siesta",50]
    
Para una necesidad Energía, otra posible salida es:
["Acostarse a dormir", 80]

Ten en cuenta que después de realizada la acción el valor de cantidad_incremento más alto que se puede alcanzar es (100 - {level}) y que mientras más bajo sea el valor de level mayor será el aumento de cantidad_incremento.
Por tanto, en cantidad incremento devuelve un valor entre [1, 100-{level}]

Ahora si, analiza la siguiente necesidad de Pedro:
Necesidad: {need}
"""
    return prompt


def human_plan_generator_prompt(intention: str):
    plan_instruction = f"""
Eres Pedro, un agente operando en una casa con varias áreas de estar y objetos con los que interactuar:

A continuación se muestra una lista de los objetos que hay en la casa:
{make_list(simulation_data.objects_names)}

Tu objetivo es, a partir de una intención que tienes (que se encuentra debajo donde dice Intención) escrita en lenguaje natural,
formar una tarea.
Esta tarea está dada por la acción ["CAMINAR_HASTA <objeto>"] según tu intención.

Tu respuesta será dada en el siguiente formato: ["CAMINAR_HASTA <objeto>"] 

Debes sustituir <objeto> por el nombre del objeto dentro de la lista de objetos que hay en la casa que más sentido tenga utilizar para completar la acción.

Ahora si, debes procesar la siguiente intención
Intención: {intention}
"""

    return plan_instruction


###################### Will-E prompts ########################
def bot_plan_generator_prompt(intention: str):
    obj_actions, area_actions = get_obj_actions(), get_area_actions()
    
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


def validate_instruction_prompt(order: str):
    obj_actions, area_actions = get_obj_actions(), get_area_actions()
    
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


def is_only_response_instruction_prompt(intention: str):
    instruction = f"""
Eres Will-E, un robot con la finalidad de asistir y apoyar a Pedro. Ambos comparten un espacio de convivencia, una casa. Todas las labores que desempeñas como robot se llevan a cabo exclusivamente dentro del entorno doméstico.

Pedro presenta una necesidad específica que se detalla a continuación en el apartado "Orden".

Tu objetivo es determinar si la necesidad de Pedro puede verse como una tarea que puedas realizar de manera autónoma, contando 
con una base de conocimientos preestablecida, que pueda ser ejecutada por ti sin necesidad de interactuar con el entorno físico que te rodea, que la puedas realizar de manera independiente.

En el caso de que la solicitud de Pedro represente una acción factible de realizar utilizando únicamente información preexistente y pueda ser respondida en lenguaje natural, responde: si

En caso de que la solicitud de Pedro pueda entenderse como una acción que requiere manipulación de objetos domésticos, responde: no

Por ejemplo:
Para la orden (Que hora es?) tu respuesta debe ser: si
Para la orden (Necesito una receta de cocina para hacer un pastel) tu respuesta debe ser: si
Para la orden (Recomiendame una película de acción por favor) tu respuesta debe ser: si
Para la orden (Pon mi lista de reproducción favortia) tu respuesta debe ser: si

Orden: {intention}
"""
    
    return instruction


def instance_query_robot_answer_prompt(intention: str):
    instruction = f"""
Eres Will-E, un robot con la finalidad de asistir y apoyar a Pedro, tanto en sus tareas domésticas como en su entretenimiento. Se creativo. Ambos comparten un espacio de convivencia, una casa.
Entre tus funcionalidades está la de ser capaz de reporducir música por un altavoz. Por lo que Pedro puede ordenarte reproducir música, a lo que deberás responder: Reproduciendo música

Pedro presenta una necesidad específica que se detalla a continuación en el apartado "Orden".

Tu objetivo es dar respuesta a la petición de Pedro en lenguaje natural. 
Sé lo más preciso y objetivo en tu respuesta.

Ten en cuenta que NO pregutarle nada a Pedro, solamente darle una respuesta explicitamente para lo que pide.
Tu respuesta siempre debe ser positiva.

Por ejemplo:
Para la orden (recominedame una canción) tu respuesta puede ser: 
    Te recomiendo "Imagine" de John Lennon
Para la orden (recominedame una canción) tu respuesta puede ser: 
    Te recomiendo "Closer" de The Chainsmokers feat. Halsey.
Para la orden (necesito una receta de batdio de plátano) tu resouesta puede ser:
    Claro, aquí tienes una receta corta para un batido de plátano:
    Ingredientes:
    1 plátano maduro
    1 taza de leche (puede ser leche de vaca, almendra, soja, etc.)
    1 cucharada de miel o azúcar (opcional)
    Hielo (opcional)
    Instrucciones:
    Pelar el plátano y cortarlo en rodajas.
    Colocar las rodajas de plátano en una licuadora.
    Agregar la taza de leche.
    Si se desea, agregar la cucharada de miel o azúcar para endulzar.
    Opcionalmente, añadir algunos cubos de hielo para una textura más fría y espesa.
    Licuar todos los ingredientes hasta obtener una mezcla suave y homogénea.
    Verter el batido en un vaso y disfrutar.
    ¡Listo! Ahora puedes disfrutar de un delicioso batido de plátano.

Orden: {intention}
"""

    return instruction


# pasarle al llm una temperatura=0.1
def bot_need_plan_generator_prompt(intention: str):
    obj_actions = get_obj_actions()
    
    plan_instruction = f"""
Eres un robot llamado Will-E, destinado a asistir y ayudar a Pedro. Ambos conviven en una casa. Todas las tareas que
cumples como robot se desarrollan dentro de la casa.

A continuación se muestra una lista de los objetos, cada objeto de la lista es sustituible por <objeto>:
{make_list(simulation_data.objects_names)}
Pedro

En la casa también está Pedro, que es la persona a la que estás destinado a ayudar.

A continuación se muestra una lista de tareas que se utilizan para elaborar un plan:
{make_list(obj_actions)}

Tu objetivo es, a partir de una orden (que se encuentra debajo donde dice Orden) en lenguaje natural,
crear un plan utilizando únicamente las tareas de la lista de tareas antes mencionada. 

Para poner una tarea en la lista debes completar la sección <objeto>.
Ten en cuenta que solo puedes utilizar objetos que estén en la lista de objetos antes mencionada y que debes seleccionar el nombre del objeto 
que más sentido tenga para la tarea que se va a realizar.

Notar que para usar un objeto hay q caminar hasta él.

Solo debes hacer tareas necesarias para completar la orden.

Además debes devolver un mensaje para Pedro, que indique que la orden ya se cumplió. El mensaje se conforma en tiempo pretérito

Por ejemplo: 
para la orden (Poner una película), tu respuesta debe ser
{{
    "tareas": ["CAMINAR_HASTA tv", "ENCENDER tv"],
    "mensaje": "Ya te he puesto una película en Netflix"
}}
para la orden (Tráeme el móvil), tu respuesta debe ser
{{
    "tareas": ["CAMINAR_HASTA móvil", "COGER móvil", "CAMINAR_HASTA Pedro", "SOLTAR móvil"],
    "mensaje": "Aquí tienes el móvil"
}}
para la orden (Prepárame un baño de espuma),tu respuesta debe ser
{{
    "tareas": ["CAMINAR_HASTA bañera", "PREPARAR bañera", "CAMINAR_HASTA Pedro"],
    "mensaje": "Tu baño de espuma ya está listo"
}}


Ahora si, debes procesar la siguiente orden
Orden: {intention}
"""
    return plan_instruction



###################### Utils ########################
def get_obj_actions():
    obj_actions = simulation_data.robot_obj_actions.copy()
    for i in range(len(obj_actions)):
        obj_actions[i] += " <objeto>"
    return obj_actions

def get_area_actions():
    area_actions = simulation_data.robot_area_actions.copy()
    for i in range(len(area_actions)):
        area_actions[i] += " <area>"
    return area_actions

def get_no_obj_actions():
    return simulation_data.robot_no_obj_actions.copy()



def make_list(arr: list):
    response = ""
    for i in arr:
        response += i
        response += "\n"

    return response
