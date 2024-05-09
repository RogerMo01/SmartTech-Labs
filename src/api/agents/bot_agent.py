import json
import random
from datetime import datetime
from agents.bdi_agent import *
from House import *
from search import *
from agents.task import *
from agents.plan import *
from llm.gemini import Gemini
from llm.prompts import *
import simulation_data

NEGATIVE_FEEDBACK = ["Lo siento, pero no puedo hacer lo que me pides",
                     "No tengo las habilidades para hacer eso, lo siento",
                     "No sé como hacer lo que me pides, lo siento"]



class Bot_Belief(Belief):
    def __init__(self, house: House = None, other_beliefs={}):
        super().__init__(house, other_beliefs)
        self.last_order: Order = None
        self.last_notice: Order = None
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
        self.current_datetime = None

    def run(self, submmit_event, current_datetime: datetime):
       self.current_datetime = current_datetime
        
       perception = self.see()
       self.brf(perception)

       self.plan_intentions()
       
       if len(self.intentions) > 0:
            current_plan: Plan = self.intentions[0]
            current_plan.run(submmit_event, current_datetime, self.beliefs.last_notice)

            if current_plan.is_successful:
                # print(f"PLAN ~{current_plan.intention_name}~ FINISHED")
                self.intentions.pop(0)
                
            self.increment_postponed_plan(current_plan)
            perception = self.see()
            self.brf(perception)
       
            _reconsider, selected_intention = self.reconsider(current_plan, 0.1)
            
            if _reconsider:
                # print(f'Will-E reconsidered his plan {current_plan.intention_name} to {selected_intention.intention_name}')
                logger.log_overtake(current_plan, selected_intention)
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
            self.beliefs.last_notice = self._detect_notice()
        else:
            self.beliefs.last_order = None

        
        self.beliefs.bot_position = perception.bot_position
        self.beliefs.human_position = perception.human_position

        return self.beliefs
    

    def plan_intentions(self):
        
        # Pedro order
        if self.beliefs.last_order is not None:
            is_valid_plan = True
            
            # Pedro order and boosts a need
            if self.beliefs.last_order.by_human_for_need:

                # Check is only response
                prompt = is_only_response_instruction_prompt(self.beliefs.last_order.body)
                only_response = self.llm(prompt)
                
                require_object = only_response == 'no'

                # Pedro order, boosts a need and is response type
                if not require_object:
                    speak_task = Speak(self.agent_id, self.human_id, self.beliefs.last_notice, self.__house, self.beliefs)

                    # prompt = instance_query_robot_answer_prompt(self.beliefs.last_order.body)
                    # response = self.llm(prompt)
                    
                    # speak_task = Speak(self.agent_id, self.human_id, self.beliefs.last_order.body, self.__house, self.beliefs, response, )
                    new_plan = Plan(f"Responder a {self.human_id}", self.__house, self.agent_id, self.beliefs, [speak_task])
                    
                    self.intentions.insert(0, new_plan)
                    return
                
                # Pedro order, boosts a need and is action type
                else:
                    bot_no_obj_prompt = bot_no_obj_action_prompt(self.beliefs.last_order.body)
                    action = self.llm(bot_no_obj_prompt)

                    # Pedro order, boosts a need, is action type and use objects
                    if action == "no":
                        # Testing not using this
                        #############################################################################
                        # validate_prompt = validate_instruction_prompt(self.beliefs.last_order.body)
                        # intention = self.llm(validate_prompt)
                        # if intention == 'No':
                        #     is_valid_plan = False
                        # else:
                        #############################################################################
                        
                        intention = self.llm(action_to_intention_prompt(self.beliefs.last_order.body))

                        try:

                            prompt = bot_need_plan_generator_prompt(intention)
                            plan = self.llm(prompt, 0.1)
                            plan = json.loads(plan)
                            tasks = plan["tareas"]
                            message = plan["mensaje"]
                            new_plan = Plan(intention, self.__house, self.agent_id, self.beliefs)
                            for t in tasks:
                                task: Task|None = self._task_parser(t)
                                if task is None: is_valid_plan = False
                                new_plan.add_task(task)
                            
                            # Notify human plan is done
                            new_plan.add_task(Speak(self.agent_id, self.human_id, None, self.__house, self.beliefs, message))
                        except:
                            is_valid_plan = False
                    
                    # Pedro order, boosts a need, is action type and don't use objects
                    else:
                        try:
                            action = json.loads(action)
                            if action[0] == simulation_data.PLAY_MUSIC:
                                play_music_task = PlayMusic(self.agent_id, action[1], None, self.__house)
                                new_plan = Plan("Reproducir música", self.__house, self.agent_id, self.beliefs, [play_music_task])
                        except:
                            is_valid_plan = False

                if not is_valid_plan:
                    # Generate negative feedback and say it to human
                    nf_speak = Speak(self.agent_id, self.human_id, None, self.__house, self.beliefs, random.choice(NEGATIVE_FEEDBACK))
                    plan = Plan("Responder no entender", self.__house, self.agent_id, self.beliefs, [nf_speak])
                    self.intentions.insert(0, plan)
                    logger.log_understand_error(self.beliefs.last_order)
                else:
                    self.intentions.append(new_plan)

            # Pedro order and don't boosts any need
            else:
                # Check is a valid order here and build intention
                prompt = validate_instruction_prompt(self.beliefs.last_order.body)
                intention = self.llm(prompt)
                if intention == "No": 
                    is_valid_plan = False
                else:
                    # Pass first filter
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
                    nf_speak = Speak(self.agent_id, self.human_id, None, self.__house, self.beliefs, random.choice(NEGATIVE_FEEDBACK))
                    plan = Plan("Responder no entender", self.__house, self.agent_id, self.beliefs, [nf_speak])
                    self.intentions.insert(0, plan)
                    logger.log_understand_error(self.beliefs.last_order)
                else:
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
            if room == "" or (task.room is not None and task.room == room):
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
            if o[0].startswith(start):
                return Order(o[0], o[1])
        return None
    
    def _detect_notice(self):
        start = f"{self.human_id} dice:"
        for o in self.beliefs.speaks:
            if o[0].startswith(start):
                return Order(o[0], o[1])
        return None

    
    def _task_parser(self, t: str):
        splited_str = t.split()
        action = splited_str[0]
        if len(splited_str) > 1:
            tag = splited_str[1]
        else:
            tag = ""   # ver que hacer aqui

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
            elif tag == "Pedro":
                # Caminar hasta Pedro
                return Move(self.agent_id, self.__house, self.beliefs, self.beliefs.human_position)


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
                if obj.portable and obj.carrier is self.agent_id:
                    return Drop(self.agent_id, obj, self.__house, self.pocket)
            
        elif action == simulation_data.SET_UP:
            if tag in simulation_data.objects_names:
                # Preparar objeto
                obj: Object = self.__house.get_object(tag)
                return TimeTask(self.agent_id, self.__house, self.beliefs, timedelta(seconds=random.randint(10, 180)), object=obj.name, type="Preparar")

        elif action == simulation_data.USE:
            if tag in simulation_data.objects_names:
                # Use some object
                obj: Object = self.__house.get_object(tag)
                return TimeTask(self.agent_id, self.__house, self.beliefs, timedelta(seconds=random.randint(10, 40)), object=obj.name, type="Preparar")

        elif action == simulation_data.PLAY_MUSIC:
            time = timedelta(seconds = 600)
            return PlayMusic(self.agent_id,time, house = self.__house)


        return None


