import json
from agents.bdi_agent import *
from agents.plan import Plan
from agents.task import *
from search import *
from agents.needs import Needs
from llm.gemini import *
from llm.llm import *
from llm.prompts import *
from simulation_data import BEST_TIMES, NEEDS_LIMIT, ENERGY, HUNGRY, HYGIENE, BLADDER, ENTERTAINMENT

SPANISH_NEEDS = {'bladder':'Vejiga','hungry':'Hambre', 'energy':'Energia', 'hygiene':'Higiene', 'entertainment':'Entretenimiento'}
NEEDS_ORDER = ['bladder', 'hungry', 'energy', 'hygiene', 'entertainment']



class Human_Belief(Belief):
    def __init__(self, house: House, other_beliefs: dict):
        super().__init__(house, other_beliefs)


class Human_Agent(BDI_Agent):
    def __init__(self, house: House, other_beliefs:dict):
        self.agent_id = 'Pedro'
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

    def  run(self, submmit_event):
        
        perception = self.see()
        self.brf(perception)

        self.plan_intentions()
        current_plan = None
        if len(self.intentions) > 0:
            current_plan: Plan = self.intentions[0]
            current_plan.run(submmit_event)

            if current_plan.is_successful:
                print("PLAN COMPLETED")
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
        self.beliefs.bot_position = perception.bot_position
        self.beliefs.human_position = perception.human_position

        return self.beliefs
    
    
    def plan_intentions(self):

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
                    selected_helper = random.uniform(0,1)
                    if selected_helper >= 0.5:
                        level = self.needs[need]
                        prompt = generate_action_values(SPANISH_NEEDS[need], level)
                        response = self.llm(prompt)
                        try:
                            response = json.loads(response)
                            level = response[1]
                            time = self.calculate_time(need, level)
                            intention_name = response[0]
                            task = human_plan_generator_prompt(intention_name)
                            task = self.llm(task, True)
                            task = json.loads(task)
                            move_task, object = self._task_parser(task[0])
                            need_task = Need(self.agent_id, time, self.__house, self.beliefs, object.name,  need, self.needs)

                            plan: Plan = Plan(intention_name, self.__house, 'Pedro', self.beliefs, [move_task,need_task], need)      # Hacer el plan

                            self.intentions.append(plan)
                            self.overtake_plan(plan)
                        except Exception as e:
                            pass
                    else:
                        # robot helps
                        level = self.needs
                        instruction = human_instruction_request_for_need_prompt(need=SPANISH_NEEDS[need])
                        instruction = self.llm(instruction, True)
                        self.__house.say(self.agent_id, instruction)



    def calculate_time(self, need, level):
        best_time = BEST_TIMES[need]  
        inc_by_second = 100 / best_time
        result = level / inc_by_second
        return timedelta(seconds=result)
    

    def reconsider(self):
        """Reconsiders intentions"""
        return False

    def overtake_plan(self, plan: Plan):
        """Overtakes plan after current head plan, according to tasks order"""
        if len(self.intentions) == 1: return
        self.intentions.remove(plan)

        index = 0
        for p in self.intentions:
            # Busca el primer plan con menor prioridad e inserta
            if p.need is None or NEEDS_ORDER.index(p.need) > NEEDS_ORDER.index(plan.need):
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
            if current_plan.need == ENERGY:

                # No bajar más del límite estos parámetros
                if self.needs[BLADDER] <= NEEDS_LIMIT[BLADDER]:
                    needs.remove(BLADDER)
                if self.needs[ENTERTAINMENT] <= NEEDS_LIMIT[ENTERTAINMENT]:
                    needs.remove(ENTERTAINMENT)

            for need in needs:
                if need != current_plan.need:
                    if not self.__house.get_is_music_playing() and need != ENTERTAINMENT:
                        self.needs.dec_level(need)

            

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