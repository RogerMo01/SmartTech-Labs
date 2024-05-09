import json
from datetime import datetime
from agents.bdi_agent import *
from agents.plan import Plan
from agents.task import *
from search import *
from agents.needs import Needs
from utils import *
from llm.gemini import *
from llm.llm import *
from llm.prompts import *
from simulation_data import BEST_TIMES, NEEDS_LIMIT, ENERGY, HUNGRY, HYGIENE, BLADDER, ENTERTAINMENT

FILE_SRC = "src/api/logs/pedro.txt"

NEEDS_ORDER = ['bladder', 'hungry', 'energy', 'hygiene', 'entertainment']
SPANISH_NEEDS = {'bladder':'Vejiga','hungry':'Hambre', 'energy':'Energia', 'hygiene':'Higiene', 'entertainment':'Entretenimiento'}

class Human_Belief(Belief):
    def __init__(self, house: House, other_beliefs: dict):
        super().__init__(house, other_beliefs)
        self.last_notice: Order = None


class Human_Agent(BDI_Agent):
    def __init__(self, house: House, other_beliefs:dict):
        self.agent_id = 'Pedro'
        self.bot_id = 'Will-E'
        self.__house = house
        # ---- Needs
        self.needs = Needs()
        # -----------
        self.beliefs = Human_Belief(house, other_beliefs) # initial beliefs
        self.desires = ["Regar la casa para que el robot la organice"]
        self.intentions: list[Plan] = []
        # self.intentions: list[Plan] =  Plan("Hacer pipi", self.__house, self.agent_id, self.beliefs, [Sleep(self.agent_id, self.__house, self.beliefs, object='cama')], need='bladder')]
        # self.intentions: list[Plan] = [Plan("Dar una vuelta por la casa",house, self.agent_id, self.beliefs, [Move(self.agent_id, house, self.beliefs, E9), Move(self.agent_id, house, self.beliefs, E5)])]
        self.llm = Gemini()
        self.last_given_order = None
        self.current_datetime = None

    def run(self, submmit_event, current_datetime: datetime):
        self.current_datetime = current_datetime

        perception = self.see()
        self.brf(perception)

        self.plan_intentions()


        #······Temporal for debug ······
        for i in self.intentions:
            if i is None:
                print(i)
                pass
        #·······························
            

        current_plan = None
        if len(self.intentions) > 0:
            current_plan: Plan = self.intentions[0]
            current_plan.run(submmit_event, current_datetime, self.beliefs.last_notice)

            if current_plan.is_successful:
                print(f"PLAN ~{current_plan.intention_name}~ FINISHED")
                self.intentions.pop(0)

        perception = self.see()
        self.brf(perception)
        self.decrease_needs(current_plan)

        if self.reconsider():
            # reevaluate intentions
            pass
        pass


    def see(self):
        """Percepts changes in enviroment"""

        perception = Perception(*self.__house.get_data())
        return perception
    
    
    def brf(self, perception):
        """Update the agent's beliefs based on the given percept.

        Args:
            percept (?): the percept of the environment
        """
        self.beliefs.map = perception.map
        self.beliefs.objects = perception.objects
        self.beliefs.speaks = perception.speaks
        
        self.beliefs.last_notice = self._detect_notice()

        self.beliefs.bot_position = perception.bot_position
        self.beliefs.human_position = perception.human_position

        return self.beliefs
    
    
    def plan_intentions(self):

        if self.beliefs.last_notice is not None:
            self.plan_with_notice()
        
        limit_exceed = self._are_there_needs_at_limit()

        if limit_exceed:
            self._create_intention_by_human()
            return

        # No plans and no limits exceed
        if not limit_exceed and len(self.intentions) == 0:

            # Decidir si hacer algo o no (cada 1 hora)
            if assert_chance(1/3600):
                need = self._get_min_need() # skips ENERGY
                # Decidir si hacerlo solo o con robot
                # if assert_chance(0.5):
                if assert_chance(0.5) or need==BLADDER: #BLADDER just as individual
                    self._create_individual_plan(need)
                else:
                    # robot helps
                    instruction = human_instruction_request_for_need_prompt(need=SPANISH_NEEDS[need])
                    instruction = self.llm(instruction, True)
                    
                    self.last_given_order = instruction
                    speak_task = Speak(self.agent_id, self.bot_id, self.beliefs.last_notice, self.__house, self.beliefs, instruction, human_need=True)
                    plan = Plan(f"Ordenar a {self.bot_id} para q ayude en +{need}+", self.__house, self.agent_id, self.beliefs, [speak_task], need=need)

                    self.register_log(f"Pedro planifica >{plan.intention_name}< preguntando >{instruction}<", True)
                    self.intentions.append(plan)
            

    def _create_intention_by_human(self):
        for need in NEEDS_ORDER:
            # Si hay necesidad a cubrir (need)
            if self.needs[need] <= NEEDS_LIMIT[need]:
                covered = False
                # Si hay plan q cubre esa necesidad en la cola
                for plan in self.intentions:
                    if plan.need == need:
                        # Comprobar orden
                        ordered = self.check_order(plan)

                        # Adelantarlo
                        if not ordered:
                            self.overtake_plan(plan)

                        covered = True
                        break

                # No hay plan adelantado => poner plan
                if not covered:
                    # Dormir solo después de las 11pm, y antes de las 4am
                    if need == ENERGY and (self.current_datetime.hour < 23 and self.current_datetime.hour > 4):
                        pass
                    else:
                        self._create_individual_plan(need)
    

    def _create_individual_plan(self, need: str):
        """Creates an individual plan for Pedro, for an especific need"""
        level = self.needs[need]
        prompt = generate_action_values(SPANISH_NEEDS[need], level, self.current_datetime)
        response = self.llm(prompt)
        try:
            response = json.loads(response)
            level = response[1]
            time = self.calculate_time(need, level)

            intention_name = response[0]

            # Sleep long time (7-8 hours)
            if need == ENERGY:
                time = timedelta(seconds=random.randint(25200, 28800))
                intention_name = random.choice(["Dormir", "Ir a dormir"])

            task = human_plan_generator_prompt(intention_name)
            task = self.llm(task, True)
            task = json.loads(task)
                
            move_task, object = self._task_parser(task[0])
            need_task = Need(self.agent_id, time, intention_name, self.__house, self.beliefs, object.name, need, self.needs)
            
            plan: Plan = Plan(intention_name, self.__house, self.agent_id, self.beliefs, [], need)
            
            # Consider ask something to Will-E at plan beginning 
            hungry_chance = need == HUNGRY and assert_chance(0.9)
            bladder_chance = need == BLADDER and assert_chance(0.1)
            hygiene_chance = need == HYGIENE and assert_chance(0.6)
            entertainment_chance = need == ENTERTAINMENT and assert_chance(0.8)
            energy_chance = need == ENERGY and assert_chance(0.6)
            #
            if hungry_chance or entertainment_chance or bladder_chance or hygiene_chance or energy_chance:
                message = pre_task_question(intention_name, self.current_datetime)
                message = self.llm(message)
                # Speak to Will-E
                ask_task = Speak(self.agent_id, self.bot_id, self.beliefs.last_notice, self.__house, self.beliefs, message, human_need=True)
                plan.add_task(ask_task)
            
            plan.add_task(move_task)
            plan.add_task(need_task)

            self.register_log(f"Pedro planifica >{plan.intention_name}<", True)
            self.intentions.append(plan)
            self.overtake_plan(plan)
        except Exception as e:
            # Did't make it
            pass


    def _are_there_needs_at_limit(self):
        for need in NEEDS_ORDER:
            if self.needs[need] <= NEEDS_LIMIT[need]:
                return True
        return False

    def plan_with_notice(self):
        if self.beliefs.last_notice is not None:
            # Veces q se intenta
            tries = 0

            # Continue in speaking
            if len(self.intentions) > 0 and len(self.intentions[0].tasks) > 0 and isinstance(self.intentions[0].tasks[0], Speak): return

            # Interpretar lo que dijo el robot
            prompt = human_intention_by_robot_response(self.last_given_order, self.beliefs.last_notice.body)
            intention = self.llm(prompt)

            # Robot confirms last human order
            order_confirmation = intention != "No"

            if order_confirmation:
                # Intentar 3 veces antes de renunciar
                while tries < 3:
                    try:
                        # Hacer  el plan con la intención
                        task = human_plan_generator_prompt(intention)
                        task = self.llm(task, True)
                        task = json.loads(task)

                        # Definir el tiempo a dedicarle
                        time_request = time_for_intention(intention)
                        time_and_need = self.llm(time_request)
                        time_and_need = json.loads(time_and_need)
                        seconds, need = time_and_need[0], time_and_need[1]

                        move_task, object = self._task_parser(task[0])
                        need_task = Need(self.agent_id, timedelta(seconds=seconds), intention, self.__house, self.beliefs, object.name, need, self.needs)

                        plan = Plan(intention, self.__house, self.agent_id, self.beliefs, [move_task, need_task], need=need)

                        self.register_log(f"Pedro planifica >{intention}<", True)
                        self.intentions.append(plan)
                        return
                    except:
                        tries+=1
                
                # No pudo interpretar lo del robot => renunciar
                pass
            
            # Robot says anything else
            else:
                # 🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
                # raise NotImplementedError("Robot says anything else")
                # Robot did't understand
                print(f"{self.agent_id} reported: {self.bot_id} me dijo ({self.beliefs.last_notice.body}) y yo había ordenado ({self.last_given_order})")
                pass


    def calculate_time(self, need, level):
        best_time = BEST_TIMES[need]  
        inc_by_second = 100 / best_time
        result = level / inc_by_second
        return timedelta(seconds=result)
    

    def reconsider(self):
        """Reconsiders intentions"""
        return False
    
    def _detect_notice(self):
        start = f"{self.agent_id} dice: Oye {self.bot_id}"
        for o in self.beliefs.speaks:
            if not o[0].startswith(start):
                return Order(o[0], o[1])
        return None

    def overtake_plan(self, plan: Plan):
        """Overtakes plan after current head plan, according to tasks order"""
        if len(self.intentions) == 1: return

        index = 0
        for p in self.intentions:
            # Busca el primer plan con menor prioridad e inserta
            if p.need is None or NEEDS_ORDER.index(p.need) > NEEDS_ORDER.index(plan.need):
                self.register_log(f"Pedro adelanta >{plan.intention_name}<")
                self.intentions.remove(plan)
                self.intentions.insert(index, plan)
                return
            index +=1

    def check_order(self, plan: Plan):
        """Checks all needs plans to be in order"""
        for p in self.intentions:
            if p == plan:
                return True
            else:
                if p.need is None or NEEDS_ORDER.index(p.need) > NEEDS_ORDER.index(plan.need):
                    return False
        raise Exception("Plan must be in intentions")
    
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
                    return Move(self.agent_id, self.__house, self.beliefs, obj.human_face_tiles[0]), obj
            
        raise Exception(f'Invalid action: {action} or object: {tag}')

    
    def decrease_needs(self, current_plan:Plan):
        needs = NEEDS_ORDER.copy()
        
        if current_plan is not None:
            # Que no baje la del plan actual
            needs.remove(current_plan.need)

            if current_plan.need == ENERGY:
                # No bajar más del límite estos parámetros
                if self.needs[BLADDER] <= NEEDS_LIMIT[BLADDER]+1:
                    if BLADDER in needs: needs.remove(BLADDER)
                if self.needs[ENTERTAINMENT] <= NEEDS_LIMIT[ENTERTAINMENT]+1:
                    if ENTERTAINMENT in needs: needs.remove(ENTERTAINMENT)
                if self.needs[HUNGRY] <= NEEDS_LIMIT[HUNGRY]+1:
                    if HUNGRY in needs: needs.remove(HUNGRY)

                # Ganas de orinar cada 12 horas durante el sueño
                if assert_chance(1/43200) and self.needs[BLADDER] <= NEEDS_LIMIT[BLADDER]+1:
                    self.needs[BLADDER] -= 2

            
            # Si hay música puesta, subir ENTERTAINMENT
            if self.__house.get_is_music_playing():
                # Evitar que baje más
                if ENTERTAINMENT in needs: needs.remove(ENTERTAINMENT)
                # Subirlo (1 hora => +20)
                self.needs.sum_level(ENTERTAINMENT, 20/3600)

        for need in needs:
            # Si la energia esta por debajo del limite, y no es entre 11 y 9, no bajar
            if need == ENERGY and (self.needs[ENERGY]<NEEDS_LIMIT[ENERGY]) and (self.current_datetime.hour < 23 or self.current_datetime.hour > 9):
                continue

            self.needs.dec_level(need)


    def _get_min_need(self):
        min = BLADDER
        min_value = self.needs.bladder
        for n in NEEDS_ORDER:
            if n == ENERGY: continue
            if self.needs[n] < min_value: 
                min = n
                min_value = self.needs[n]
        return min


    def options(self):
        pass

    def filter(self):
        pass

    def reconsider(self):
        pass

    def set_plan(self):
        pass

    def get_plan(self):
        pass

    def excecute(self, action):
        pass
        
    def register_log(self, text: str, show_intentions = False):
        with open(FILE_SRC, 'a', encoding='utf-8') as file:
            text = f"[{self.current_datetime.strftime('%Y-%m-%d %H:%M:%S')}] {text}"
            file.write(text + '\n')
            # if show_intentions:
            #     file.write(f"Intentions: {self.intentions}" + '\n\n')
