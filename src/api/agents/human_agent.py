from agents.bdi_agent import *
from agents.plan import Plan
from agents.task import *
from search import *
from agents.needs import Needs


NEEDS_ORDER = ['bladder', 'hungry', 'energy', 'hygiene', 'entertainment']
NEEDS_LIMIT = {'bladder': 20, 'hungry': 30, 'energy': 15, 'hygiene': 30, 'entertainment': 10}


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
        self.intentions: list[Plan] = [Plan("Dormir", self.__house, self.agent_id, self.beliefs, [Sleep(self.agent_id, self.__house, self.beliefs, object='cama')], need='energy'),
                                       Plan("Hacer pipi", self.__house, self.agent_id, self.beliefs, [Sleep(self.agent_id, self.__house, self.beliefs, object='cama')], need='bladder')]
        # self.intentions: list[Plan] = [Plan("Dar una vuelta por la casa",house, self.agent_id, self.beliefs, [Move(self.agent_id, house, self.beliefs, E9), Move(self.agent_id, house, self.beliefs, E5)])]


    def  run(self, submmit_event):
        
        perception = self.see()
        self.brf(perception)

        self.plan_intentions()
    
        if len(self.intentions) > 0:
            current_plan: Plan = self.intentions[0]
            current_plan.run(submmit_event)

            if current_plan.is_successful:
                print("PLAN COMPLETED")
                self.intentions.pop(0)
        
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

                    ########################################
                    plan: Plan = Plan()      # Hacer el plan
                    ########################################

                    self.intentions.append(plan)
                    self.overtake_plan(plan)






    def overtake_plan(self, plan: Plan):
        """Overtakes plan after current head plan, according to tasks order"""
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