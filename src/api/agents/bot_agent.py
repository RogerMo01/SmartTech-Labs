import json
from agents.bdi_agent import *
import random
from House import *
from search import *
from agents.task import *
from agents.plan import *
from llm.gemini import Gemini
from llm.prompts import bot_plan_generator_prompt, validate_instruction_prompt
import simulation_data

NEGATIVE_FEEDBACK = ["Lo siento, pero no puedo hacer lo que me pides",
                     "No tengo las habilidades para hacer eso, lo siento",
                     "No sé como hacer lo que me pides, lo siento"]

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
        self.pocket = []
        self.beliefs = Bot_Belief(house, other_beliefs) # initial beliefs
        self.desires = ["Ayudar al humano en todo lo que pueda, en el hogar"]
        self.intentions: list[Plan] = []
        # self.intentions: list[Plan] = [Plan("Mojar una mata", house, self.agent_id, self.beliefs, [UseWater(self.agent_id, house, self.beliefs, timedelta(seconds=10), object=plant1.name)])]
                                        # Plan("Limpiar el cuarto", house, self.agent_id, self.beliefs,[Clean(self.agent_id, house, self.beliefs, timedelta(seconds=10), 'bedroom')])]
        # self.intentions: list[Plan] = [Plan("Dar una vuelta por la casa", house, self.agent_id, self.beliefs, [Move(self.agent_id, house, self.beliefs, E8), Move(self.agent_id, house, self.beliefs, A0)]),
        #                              Plan("Limpiar el cuarto", house, self.agent_id, self.beliefs,[Clean(self.agent_id, house, self.beliefs, timedelta(seconds=10), 'bedroom')])]


    def run(self, submmit_event):
        
       perception = self.see()
       self.brf(perception)

       self.plan_intentions()
       
       if len(self.intentions) > 0:
            current_plan: Plan = self.intentions[0]
            current_plan.run(submmit_event)

            if current_plan.is_successful:
                print("PLAN COMPLETED")
                self.intentions.pop(0)
                
            self.increment_postponed_plan(current_plan)
            perception = self.see()
            self.brf(perception)
       
            _reconsider, selected_intention = self.reconsider(current_plan, 0.1)
            
            if _reconsider:
                print(f'Will-E reconsidered his plan {current_plan.intention_name} to {selected_intention.intention_name}')
                self.reorder_intentions(selected_intention, current_plan)
        

        
    def see(self):
        """Percepts changes in enviroment"""

        perception = Perception(*self.__house.get_data())
        return perception
    
    def reorder_intentions(self, selected_intention, prev_intention: Plan):
        for task in prev_intention.tasks:
            task.is_postponed = True
        
        self.intentions.remove(selected_intention)
        self.intentions.insert(0, selected_intention)


    def brf(self, perception: Perception):
        """Update the agent's beliefs based on the given percept.

        Args:
            perception (Perception): the perception of the environment
        """
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
            is_valid_plan = True
            
            # Check is a valid order here and build intention
            prompt = validate_instruction_prompt(self.beliefs.last_order)
            intention = self.llm(prompt)
            if intention == "No": 
                is_valid_plan = False
            else:
                # Then make plan
                prompt = bot_plan_generator_prompt(intention)
                try:
                    plan = self.llm(prompt)
                    plan = json.loads(plan)
                    new_plan = Plan(intention, self.__house, self.agent_id, self.beliefs)
                    for t in plan:
                        task: Task|None = self._task_parser(t)
                        if task is None: is_valid_plan = False
                        new_plan.add_task(task)

                except:
                    is_valid_plan = False

            if not is_valid_plan:
                # Generate negative feedback and say it to human
                self.__house.say(self.agent_id, random.choice(NEGATIVE_FEEDBACK))
                return

            self.intentions.append(new_plan)
            



    def reconsider(self, current_plan: Plan, probability: float):
        _reconsider = random.uniform(0,1)
        posible_plans = []
        if _reconsider <= probability:
            for intention in self.intentions:
                if self.beliefs.bot_position.area == self.get_room_plan(intention) and intention.intention_name != current_plan.intention_name:
                    posible_plans.append(intention)
            
            if len(posible_plans) != 0:
                selected_plan = random.randint(0, len(posible_plans) - 1)
                return True, posible_plans[selected_plan]
            else: return False, None

        else: return False, None

    def get_room_plan(self, plan: Plan):
        room = ""
        for task in plan.tasks:
            if room == "" or task.room == room:
                room = task.room
            else:
                return ""
        return room
    
    def increment_postponed_plan(self, current_intention: Plan):
        for intention in self.intentions:
            if intention.intention_name != current_intention.intention_name:
                for task in intention.tasks:
                    if task.is_postponed:
                        one_step = timedelta(seconds=1)
                        task.postponed_time += one_step


    # -------------- #
    # Unused methods #
    # -------------- #

    def filter(self, beliefs, desire, intentions):  # i'll use this method later
            """return the filtered intentions based on the beliefs and selected desire

            Args:
                beliefs (list): all beliefs of the agent
                desire (str): chosen desire
                intentions (list): all intentions of the agent
            """
            for i in intentions:
                if i == desire:
                    return i
            pass

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
                return o
        return None
    
    def _task_parser(self, t: str):
        splited_str = t.split()
        action = splited_str[0]
        tag = splited_str[1]

        if action == simulation_data.WALK:
            # Caminar
            if tag in simulation_data.objects_names:
                # Caminar a un objeto
                obj: Object = self.__house.get_object(tag)
                if obj.carrier is None:
                    return Move(self.agent_id, self.__house, self.beliefs, obj.robot_face_tiles[0])
            elif tag in simulation_data.areas:
                # Caminar a un area
                return Move(self.agent_id, self.__house, self.beliefs, self.__house.get_room_tile(self.agent_id, tag))

        elif action == simulation_data.CLEAN:
            # Limpiar
            if tag in simulation_data.objects_names:
                # Limpiar un objeto
                time = timedelta(seconds=5)
                obj: Object = self.__house.get_object(tag)
                if obj.cleanable:
                    return Clean(self.agent_id, self.__house, self.beliefs, time, object=obj.name)
            elif tag in simulation_data.areas:
                # Limpiar un area
                time = timedelta(seconds=10)
                return Clean(self.agent_id, self.__house, self.beliefs, time, room=tag) 
               
        elif action == simulation_data.WATER_OBJ:
            if tag in simulation_data.objects_names:
                # Echar agua a un objeto
                time = timedelta(seconds=4)
                obj: Object = self.__house.get_object(tag)
                if obj.waterable:
                    return UseWater(self.agent_id, self.__house, self.beliefs, time, object=obj.name)

        elif action == simulation_data.ON_OBJ:
            if tag in simulation_data.objects_names:
                # Encender un objeto
                time = timedelta(seconds=2)
                obj: Object = self.__house.get_object(tag)
                if obj.switchable:
                    return TimeTask(self.agent_id, self.__house, self.beliefs, time, object=obj.name, type="Encender")

        elif action == simulation_data.OFF_OBJ:
            if tag in simulation_data.objects_names:
                # Encender un objeto
                time = timedelta(seconds=2)
                obj: Object = self.__house.get_object(tag)
                if obj.switchable:
                    return TimeTask(self.agent_id, self.__house, self.beliefs, time, object=obj.name, type="Apagar")

        elif action == simulation_data.TAKE_OBJ:
            if tag in simulation_data.objects_names:
                # Tomar objeto
                obj: Object = self.__house.get_object(tag)
                if obj.portable and obj.carrier is None:
                    return Take(self.agent_id, obj, self.__house, self.pocket)

        elif action == simulation_data.DROP_OBJ:
            if tag in simulation_data.objects_names:
                # Soltar objeto
                obj: Object = self.__house.get_object(tag)
                return Drop(self.agent_id, obj, self.__house, self.pocket)

        return None

        
