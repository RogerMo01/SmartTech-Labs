from agents.bdi_agent import *
from agents.plan import Plan
from agents.task import *
from search import *

class Human_Belief(Belief):
    def __init__(self, house: House, other_beliefs: dict):
        super().__init__(house, other_beliefs)


class Human_Agent(BDI_Agent):
    def __init__(self, house: House, other_beliefs:dict):
        self.agent_id = 'Human'
        self.beliefs = Human_Belief(house, other_beliefs) # initial beliefs
        self.desires = ["Regar la casa para que el robot la organice"]
        self.intentions: list[Plan] = [Plan("Dar una vuelta por la casa",house, self.agent_id, [Move(self.agent_id, house, E9), Move(self.agent_id, house, E5)])]


    def  run(self, submmit_event):
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
        pass

    def brf(self, percept):
        """Update the agent's beliefs based on the given percept.

        Args:
            percept (?): the percept of the environment
        """
        pass

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