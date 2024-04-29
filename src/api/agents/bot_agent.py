import json
from agents.bdi_agent import *
import random
import queue
from House import *
from search import *
from agents.task import *
from agents.plan import *
from llm.gemini import Gemini
from llm.prompts import plan_generator_prompt
import simulation_data

class Bot_Belief(Belief):
    def __init__(self, house: House = None, other_beliefs={}):
        super().__init__(house, other_beliefs)
        self.last_order = None
        # self.map
        # self.likes
        # self.dislikes
        # self.constraints
        


class Bot_Agent(BDI_Agent):
    ACTIONS = ['Move to sofa', 'Move to chair1'] # for testing purposes 

    def __init__(self, house: House, other_beliefs: dict):
        # super().__init__(beliefs, intentions)
        self.__house = house    # private attribute
        self.agent_id = 'Will-E'
        self.human_id = 'Pedro'
        self.llm = Gemini()
        self.beliefs = Bot_Belief(house, other_beliefs) # initial beliefs
        self.desires = ["Ayudar al humano en todo lo que pueda, en el hogar"]
        self.intentions: list[Plan] = []
        # self.intentions: list[Plan] = [Plan("Dar una vuelta por la casa", house, self.agent_id, self.beliefs, [Move(self.agent_id, house, self.beliefs, E8), Move(self.agent_id, house, self.beliefs, A0)]),
        #                             Plan("Limpiar la cocina", house, self.agent_id, self.beliefs,[Clean(self.agent_id, house, self.beliefs, 'bedroom')])]


    def run(self, submmit_event):
        # Percibir lo nuevo del entorno
        # en base a las percepciones actualizar mis creencias y actualizar mi lista de intenciones (considerar)
        # (actualmente como no se percibe nada nuevo, no es necesario esto)

        # perceptions = self.percept()
        # self.beliefs = self.brf(perceptions)

        # Plans already in queue
        perception = self.see()
        self.brf(perception)

        self.plan_intentions()
        
        if len(self.intentions) > 0:
            current_plan: Plan = self.intentions[0]
            current_plan.run(submmit_event)

            if current_plan.is_successful:
                print("PLAN COMPLETED")
                self.intentions.pop(0)
            
            # Despues de q se ejecuta, avanza un paso en el plan, reconsiderar intenciones
        if self.reconsider():
            # reevaluate intentions
            pass
        

        
    def see(self):
        """Percepts changes in enviroment"""

        perception = Perception(*self.__house.get_data())
        return perception
    

    def brf(self, perception: Perception):
        """Update the agent's beliefs based on the given percept.

        Args:
            percept (?): the percept of the environment
        """
        # al final esta funcion para esta simulacion no la necesitamos mucho
        # a no ser analizar cuando la persona tambien modifique el mapa.
        # ya, aqui se va a actualizar belief, que tendra un last_order

        self.beliefs.map = perception.map
        self.beliefs.objects = perception.objects

        # Detected new conversations
        detected_conversations = self._are_new_conversations(perception)

        self.beliefs.speaks = perception.speaks

        # Set last order
        if detected_conversations:
            self.beliefs.last_order = self._detect_order()
        else:
            self.beliefs.last_order = None

        
        self.beliefs.bot_position = perception.bot_position
        self.beliefs.human_position = perception.human_position

        return self.beliefs
    

    def plan_intentions(self):

        if self.beliefs.last_order is not None:

            # Check is a valid order here and build intention
            intention = self.beliefs.last_order

            # Then make plan
            prompt = plan_generator_prompt(intention)
            plan = self.llm(prompt)
            plan = json.loads(plan)

            new_plan = Plan(intention, self.__house, self.agent_id, self.beliefs)
            for t in plan:
                task: Task = self._action_object_parser(t)
                new_plan.add_task(task)

            self.intentions.append(new_plan)
            


    def options(self):
        """Return the chosen desire based on the beliefs and intentions"""
        #r = random.randint(0, len(intentions)-1)  # agregar criterios para elegir deseo aquí
        r = 0
        return self.intentions[r]

    # def filter(self, beliefs, desire, intentions):  # i'll use this method later
    #     """return the filtered intentions based on the beliefs and selected desire

    #     Args:
    #         beliefs (list): all beliefs of the agent
    #         desire (str): chosen desire
    #         intentions (list): all intentions of the agent
    #     """
    #     for i in intentions:
    #         if i == desire:
    #             return i
    #     pass

    def reconsider(self):
        # if self.beliefs == general_beliefs i should do something like this
        return False


    def _are_new_conversations(self, perception: Perception):
        new_conversations = False
        try:
            for i in range(len(perception.speaks)):
                if perception.speaks[i] != self.beliefs.speaks[i]:
                    new_conversations = True
        except IndexError:
            new_conversations = True
        return new_conversations

    def _detect_order(self):
        start = f"{self.human_id} dice: Oye {self.agent_id}"
        for o in self.beliefs.speaks:
            if o.startswith(start):
                return o[len(start) + 2:]
        return None
    
    def _action_object_parser(self, t: str):
        splited_str = t.split()
        action = splited_str[0]
        tag = splited_str[1]

        if action == simulation_data.WALK_OBJ:
            # Caminar
            if tag in simulation_data.objects_names:
                # Caminar a un objeto
                obj: Object = self.__house.get_object(tag)
                return Move(self.agent_id, self.__house, self.beliefs, obj.face_tiles[0])
            elif tag in simulation_data.areas:
                # Caminar a un area
                pass
        elif action in simulation_data.robot_time_actions:
            # Esperar un time (Limpiar, Echar agua)
            if tag in simulation_data.objects_names:
                # Echar agua a objeto
                pass
            elif tag in simulation_data.areas:
                # Limpiar
                pass
        elif action == simulation_data.ON_OBJ:
            # Encender algo
            pass
        elif action == simulation_data.OFF_OBJ:
            # Apagar algo
            pass
        elif action == simulation_data.TAKE_OBJ:
            # Tomar objeto
            pass
        elif action == simulation_data.DROP_OBJ:
            # Soltar objeto
            pass
        else:
            return Task(self.agent_id, timedelta(seconds=0))

