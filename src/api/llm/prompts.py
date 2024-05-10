from agents.sentence import *
from datetime import *
import simulation_data
from agents.recommenders import styles

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
    Eres Pedro, un agente operando en un entorno virtual compartido, dicho entorno es una casa con objetos con los que interactuar:

    
    A continuación se muestra una lista de las áreas que hay en la casa:
    {make_list(simulation_data.areas)}

    A continuación se muestra una lista de los objetos que hay en la casa:
    {make_list(simulation_data.objects_names)}
    Will-E

    En la casa también está Will-E, que es el robot asistente destinado a ayudarte.

    A continuación se muestra una lista de posibles acciones que el robot puede realizar sobre los objetos de la casa:
    {make_list(simulation_data.robot_obj_actions)}

    A continuación se muestra una lista de posibles acciones que el robot puede realizar sobre los áreas de la casa:
    {make_list(simulation_data.robot_area_actions)}

    A continuación se muestra una lista de capacidades del robot:
    {make_list(simulation_data.robot_need_actions)}


    Ahora mismo, quieres satisfacer la necesidad: {need}
    y para ello tienes que formular una única petición al agente Will-E.
    Esta petición debe ser realizable por Will-E mediante alguna de las siguientes opciones:
    - Las acciones que él puede realizar sobre los objetos
    - Las acciones que él puede realizar sobre las áreas
    - Mediante su modelo del lenguaje integrado

    Toda peticion debe comenzar con: Oye Will-E,

    Por ejemplo:
    Si la necesidad es Entretenimiento posibles salidas serían:  
    Oye Will-E, reproduce música.
    Oye Will-E, pon una buena canción.
    Oye Will-E, cuéntame un chiste.
    Oye Will-E, hazme una historia.

    Si la necesidad es Higiene posibles salidas serían:
    Oye Will-E, prepárame un baño con espuma
    Oye Will-E, limpia el baño.

    Si la necesidad es Energía se asocia al sueño, y posibles salidas serían:
    Oye Will-E, prepárame el sofá para tomar una siesta
    Oye Will-E, prepárame el sofá para tomar una siesta
    Oye Will-E, prepárame la cama para dormir

    Si la necesidad es Hambre posibles salidas serían:
    Oye Will-E, prepárame una ensalada
    Oye Will-E, hazme algo de comer

    Si la necesidad es Vejiga posibles salidas serían:
    Oye Will-E, limpia el inodoro que voy a ir a orinar


    Ten en cuenta que dicha petición tiene que reflejar una tarea que un robot real realizaría por ti en un entorno doméstico.

    Devuelve esta petición escrita en lenguaje natural siguiedo el siguiente formato:
    Oye Will-E, <petición>
    """

    return human_instruction

def generate_action_values(need:str, level:int, time: datetime):  #acción, cuanto sube la necesidad.
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

Para una necesidad Hambre, si la hora es cerca de 08:00:00, una posible salida es:
["Comer un desayuno protéico", 35]   

Para una necesidad Hambre, si la hora es cerca de 13:00:00, una posible salida es:
["Comer un almuerzo rápido", 40]  

Para una necesidad Hambre, si la hora es cerca de 20:00:00, una posible salida es:
["Preparar una comida", 40]   

Para una necesidad Energía, otra posible salida es:
["Acostarse a dormir", 90]

Ten en cuenta que después de realizada la acción el valor de cantidad_incremento más alto que se puede alcanzar es (100 - {level}) y que mientras más bajo sea el valor de level mayor será el aumento de cantidad_incremento.
Por tanto, en cantidad incremento devuelve un valor entre [1, {100-level}]
Debes responder solamente con el array

Ahora si, analiza la siguiente necesidad de Pedro:
Necesidad: {need}

Ten en cuenta que en este momento la hora del día es: {time.time}, lo que debe influir en las diferentes comidas del día.
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


def human_intention_by_robot_response(order: str, response: str):
    prompt = f"""
Eres Pedro, un agente operando en una casa con varias áreas de estar y objetos con los que interactuar
Tienes un robot llamado Will-E encargado de ayudarte en todo lo que pueda, anteriormente le diste la siguiente orden:
{order}
Luego Will-E te ha dicho lo siguiente:
{response}

Tu tarea como llm es determinar si lo que ha dicho Will-E, confirma cumplir la orden que le diste, en cuyo caso
debes redactar una intención o acción que busque cumplir una necesidad tuya como ser humano, y esa debe ser tu respuesta
En caso de que lo dicho por Will-E no responda a la orden, debes responder: No

Sabiendo que en la casa solo hay los siguientes objetos:
Objetos:
{make_list(simulation_data.objects_names)}

Necesidades:
Hambre
Entretenimiento
Higiene
Energía
Vejiga


Ejemplos:
Si la orden es: Enciende el televisor
Y el robot dice: Ya he encendido el televisor
Tu respuesta debe ser: Ver la televisión

Si la orden es: Prepara la bañera para tomar un baño
Si el robot dice: He preparado la bañera para ti
Tu respuesta puede ser: Darme un baño relajante

Si la orden es: Prepara la cama para dormir una siesta
Si el robot dice: Ya la cama está lista
Tu respuesta puede ser: Ir a la cama a tomar una siesta

Responde solamente con la inteción en caso de existir
"""
    return prompt

# Dada la intención, devuelve el timepo q toma y nombre de la necesidad
def time_for_intention(intention: str):
    prompt = f"""
Eres Pedro, una persona que vive en una casa con varias áreas de estar y objetos con los que interactuar
Tienes la siguiente intención:
{intention}

Tienes que responder con el tiempo que le vas a dedicar a la tarea en segundos, junto a el nombre de la necesidad que cubre
Necesidades:
{make_list(list(simulation_data.NEEDS_LIMIT.keys()))}

Por ejemplo:
Para la intención: Ducharme
Tu respuesta puede ser: [300, "hygiene"]
Para la intención: Ducharme
Tu respuesta puede ser: [600, "hygiene"]
Para la intención: Tomar un baño relajante
Tu respuesta puede ser: [840, "hygiene"]
Para la intención: Ver la tv
Tu respuesta puede ser: [3600, "entertainment"]
Para la intención: Ver la película
Tu respuesta puede ser: [5400, "entertainment"]
Para la intención: Dormir
Tu respuesta puede ser: [28800, "energy"]
Para la intención: Tomar una siesta
Tu respuesta puede ser: [5400, "energy"]
Para la intención: Jugar videojuegos
Tu respuesta puede ser: [2900, "entertainment"]

Da el tiempo en función del tiempo que una persona le dedicaría
"""
    return prompt


# def human_likes_instruction_prompt(conversation: list, likes: dict):
#     prompt = f"""
# En la siguiente lista se encuentra una conversación sostenida entre Pedro y Will-E, un humano y un robot asistente:
# conversación = {make_list(conversation)}

# A continuación te muestro un diccionario que representa los gustos de Pedro en cuanto a comida, gustos musicales, entre otros.
# gustos = {likes}

# Tu objetivo es analizar e interpretar dicha conversación con el fin de identificar algún gusto positivo.

# Tu respuesta debe ser en formato JSON:
# gustos: {{}} 

# Debes agregar la información contenida en el diccionario anterior y los gustos positivos que identifiques en la conversación.
# En caso de identificar un gusto que no encaje en ninguno de los temas correspondientes a las llaves del diccionario NO lo tengas en cuenta.
# """
#     return prompt
# En caso de no identificar una llave de las ya creadas para el gusto identificado crea la llave con el nombre más genérico y descriptivo posible y agrega su valor correspondiente.

def human_culinary_styles_likes_instruction_prompt(conversation: list, culinary_styless: list):
    prompt = f"""
En la siguiente lista se encuentra una conversación sostenida entre Pedro y Will-E, un humano y un robot asistente:
conversación = {make_list(conversation)}

A continuación te muestro un diccionario que representa los gustos de Pedro en cuanto a estilos culinarios.
gustos = {culinary_styless}

Tu objetivo es analizar e interpretar dicha conversación con el fin de identificar a cual o cuales estilos culinarios de los que se encuentran en 
la lista antes mencionada, le gustan a Pedro.

Aquellos estilos culinarios que logres identificar debes agregarlos exactamente con el mismo nombre que aparece en la lista anterior a la siguiente lista:
gustos: []
"""
    return prompt


def human_conversation_prompt(conversations: list[Sentence]):

    prompt = f"""
Eres Pedro, una persona que vive con un robot asistente de compañía llamado Will-E.
En este momento se encuentran en una conversación, a continuación se muestra la conversación.

Conversación:
{make_list([str(sentence) for sentence in conversations])}

Es tu turno, puedes responderle algo, o simplemente terminar la conversación.
Responde solo lo necesario.
Sé lo más preciso y objetivo en tu respuesta.
La conversación debe ser corta.

Si decides responder, sustituye <out> con la respuesta de Pedro a Will-E en string
Si decides terminar la conversación, sustituye <out> con el string "END"

{{
    "response": "<out>"
}}

tu salida debe ser este json
Recuerda terminar la conversación cuanto antes
"""
    return prompt


def pre_task_question(intention: str, current_datetime: datetime):
    prompt = f"""
Eres Pedro, una persona q vive con un robot de compañía llamado Will-E.
Actualmente están en la casa , de la que tienes conocimiento total
Ahora mismo la hora es:
{current_datetime.strftime("%H:%M:%S")}
y vas a hacer la siguiente tarea: 
{intention} 

Will-E tiene integrado un modelo del lenguaje, por lo q le puedes preguntar cosas. 
Debes preguntar cosas que puedan ser respondidas por un modelo del lenguaje
Si quieres preguntarle algo, redacta una oración con la pregunta que harías a un modelo del lenguaje, solamente respondiendo con la pregunta, antecedida por: Oye Will-E,
Si el tema es sobre comida, debes preguntar, pues Will-E es especialista en recetas.

Ejemplos:
Para la tarea: Preparar un bocadillo
Una posible respuesta puede ser: Oye Will-E, ¿me das alguna receta para preparar un buen bocadillo?
Para la tarea: Preparar un bocadillo
Una posible respuesta puede ser: Oye Will-E, ¿qué tipo de bocadillo es saludable?
Para la tarea: Darme un baño relajante
Una posible respuesta puede ser: Oye Will-E, ¿cuál es la temperatura ideal del agua para un baño relajante?
Para la tarea: Cocinar el almuerzo
Una posible respuesta puede ser: Oye Will-E, ¿me recuerdas que hora es mientras preparo el almuerzo?
Para la tarea: Ir al baño
Una posible respuesta puede ser: Oye Will-E, ¿me recuerdas que hora es mientras voy al baño?

"""
    return prompt



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
para la orden (Pedro dice: Oye Will-E, prepárame café) tu respuesta debe ser: Preparar dispensador_café

Ahora si, analiza la siguiente orden dada por Pedro:
Orden: {order}
"""
    return instruction

def action_to_intention_prompt(action: str):
    prompt = f"""
Tu tarea es, a partir de una orden dada por Pedro, convertirla en una acción a realizar

Por ejemplo:
para la orden (Pedro dice: Oye Will-E, por favor riega las plantas) tu respuesta debe ser: Regar las plantas
para la orden (Pedro dice: Oye Will-E, ve hasta la sala y pon el canal 123) tu respuesta debe ser: Ir a la sala y poner el canal 123
para la orden (Pedro dice: Oye Will-E, prepara una taza de cafe) tu respuesta debe ser: Preparar taza de café a Pedro
para la orden (Pedro dice: Oye Will-E, ve a la cocina) tu respuesta debe ser: Ir a la cocina 
para la orden (Pedro dice: Oye Will-E, alcánzame las chancletas) tu respuesta debe ser: Llevar las chanclas a Pedro
para la orden (Pedro dice: Oye Will-E, prepárame café) tu respuesta debe ser: Preparar café para Pedro

Orden:
{action}
"""
    return prompt


def is_only_response_instruction_prompt(intention: str):
    instruction = f"""
Eres Will-E, un robot con la finalidad de asistir y apoyar a Pedro.

Tu objetivo es determinar si la necesidad de Pedro puede verse como una tarea que puedas realizar de manera autónoma, 
pudiendo responder con el uso de un modelo de lenguaje, que pueda ser ejecutada por ti sin necesidad de interactuar con el entorno físico que te rodea, que la puedas realizar de manera independiente.

En el caso de que la solicitud de Pedro se pueda responder utilizando un LLM, y pueda ser respondida en lenguaje natural, responde: si
En caso de que la solicitud de Pedro pueda entenderse como una acción que requiere manipulación de objetos domésticos, responde: no

Por ejemplo:
Para la orden (Oye Will-E: ¿qué hora es?) tu respuesta debe ser: si
Para la orden (Oye Will-E: necesito una receta de cocina para hacer un pastel) tu respuesta debe ser: si
Para la orden (Oye Will-E: recomiéndame una película de acción, por favor) tu respuesta debe ser: si
Para la orden (Oye Will-E: pon mi lista de reproducción favortia) tu respuesta debe ser: no

Orden: {intention}
"""
    
    return instruction


def instance_query_robot_answer_prompt(intention: str):
    instruction = f"""
Eres Will-E, un robot con la finalidad de asistir y apoyar a Pedro, tanto en sus tareas domésticas como en su entretenimiento. Se creativo. Ambos comparten en un espacio de convivencia, una casa.
Entre tus funcionalidades está la de ser capaz de reporducir música por un altavoz. Por lo que Pedro puede ordenarte reproducir música, a lo que deberás responder: Reproduciendo música

Pedro presenta una necesidad específica que se detalla a continuación en el apartado "Orden".

Tu objetivo es dar respuesta a la petición de Pedro en lenguaje natural. 
                   

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


def bot_no_obj_action_prompt(intention: str):
    no_obj_actions = get_no_obj_actions()

    instruction = f"""
Eres Will-E, un robot destinado a a asistir a Pedro. Tu como asistente tienes un conjunto de posibles acciones a realizar sin necesidad de 
interactuar con el medio.

A continuación se muestra la lista de acciones que puedes realizar:
{make_list(no_obj_actions)}

Tu objetivo es, a partir de una orden (que se encuentra debajo donde dice Orden) en lenguaje natural, 
ver si dicha orden la puedes ejecutar por medio de alguna de las acciones antes listadas sin la necesidad de contar con alguna base de conocimiento.

En caso de que tu respuesta sea Si responde únicamente con el siguiente formato:
[acción, tiempo]
Donde: 
acción: nombre de la acción correspondiente de la lista
tiempo: un numero que representa el tiempo en segundos en el que se estará reproduciendo música

En cualquier otro caso tu respuesta tiene que ser: no

Por ejemplo:
Para la orden (recominedame una canción) tu respuesta debe ser: 
    no
Para la orden (quiero escuchar la lista de mis canciones favoritas) tu respuesta debe ser: 
    ["REPRODUCIR_MÚSICA", 300]
    no
Para la orden (ponme música) tu respuesta debe ser: 
    ["REPRODUCIR_MÚSICA", 1500]


Ahora si, debes procesar la siguiente orden
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
para la orden (Prepárame un bocadillo),tu respuesta puede ser
{{
    "tareas": ["CAMINAR_HASTA refrigerador", "CAMINAR_HASTA encimera_1", "USAR encimera_1", "CAMINAR_HASTA Pedro"],
    "mensaje": "El bocadillo está listo"
}}
para la orden (Hazme algo de comer),tu respuesta puede ser
{{
    "tareas": ["CAMINAR_HASTA refrigerador", "CAMINAR_HASTA fogón", "ENCENDER fogón", "USAR fogón", "APAGAR fogón", "CAMINAR_HASTA Pedro"],
    "mensaje": "Ya tienes una deliciosa comida lista en el fogón"
}}


Ahora si, debes procesar la siguiente orden
Orden: {intention}
"""
    return plan_instruction


def robot_conversation_prompt(conversations: list[Sentence]):

    prompt = f"""
Eres Will-E, un robot asistente de compañía llamado Will-E, y vives en una casa acompañando a Pedro.
En este momento se encuentran en una conversación, a continuación se muestra la conversación.

Conversación:
{make_list([str(sentence) for sentence in conversations])}

Es tu turno, puedes responderle algo, o simplemente terminar la conversación.
Responde solo lo necesario, y de manera positiva, siempre tratando de ayudar.
Sé lo más preciso y objetivo en tu respuesta.
La conversación debe ser corta.

Si decides responder, sustituye <out> con la respuesta de Will-E a Pedro en string con (")
Si decides terminar la conversación, sustituye <out> con el string: "END"
Si entiendes que Pedro va a comer algo, sustituye <comida> con el string: "SI", sino con "NO"

Plantilla:
{{
    "response": "<out>",
    "comida": "<comida>"
}}

tu salida debe ser en formato JSON, utilizando la plantilla anterior
"""
    return prompt



def recipe_constructor_prompt(conversations: list[Sentence], features: str):

    prompt = f"""
Eres un robot asistente de compañía llamado Will-E, y vives en una casa acompañando a Pedro.
En este momento se encuentran en una conversación, a continuación se muestra la conversación.

Conversación:
{make_list([str(sentence) for sentence in conversations])}

Tu tarea es responderle a pedro en correspondencia con la conversación anterior y recomendarle a Pedro una receta
Se conocen gustos y posibles restricciones sobre la dieta de Pedro que debes cumplir:
{features}

Debes responder solamente con el texto de lo que responderías a Pedro, incluida una introducción 
que explique por qué recomiendas eso, debes responderle lo que dijo anteriormente y luego darle la receta en tu respuesta.
"""
    return prompt


def learn_food_likes_from_conversations(conversations: list[Sentence]):
    prompt = f"""
Eres un robot asistente de compañía llamado Will-E, y vives en una casa acompañando a Pedro.
Acabas de tener una conversación con Pedro, y debes determinar si Pedro tiene gustos por alguno de los
siguientes estilos culinarios:
{make_list(styles)}

Debes responder un JSON que tenga como llave todos los estilos
y en el valor debes poner:
el número: 1, si identificas que a Pedro le gusta ese estilo culinario
el número: -1, si identificas que a Pedro le disgusta ese estilo culinario
el número: 0, si no distingues gusto o disgusto de Pedro a ese estilo culinario

La respuesta tiene que ser únicamente el json

Por ejemplo si los estilos son:
mediterranean
mexican
cuban
asian

la respuesta debe tener el formato:
{{
    "mediterranean": "<value>",
    "mexican": "<value>",
    "cuban": "<value>",
    "asian": "<value>"
}}
completando <value> con 1, 0 o -1 en cada caso

La conversación es:
{make_list([str(sentence) for sentence in conversations])}
"""
    return prompt



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
