from agents.bdi_agent import *
from agents.plan import Plan
from agents.task import *
from search import *


class Need:
    def __init__(self):
        self.energy = 60
        self.hungry = 60
        self.bladder = 60
        self.hygiene = 60

class Human_Belief(Belief):
    def __init__(self, house: House, other_beliefs: dict):
        super().__init__(house, other_beliefs)


class Human_Agent(BDI_Agent):
    def __init__(self, house: House, other_beliefs:dict):
        self.agent_id = 'Pedro'
        self.__house = house
        self.beliefs = Human_Belief(house, other_beliefs) # initial beliefs
        self.desires = ["Regar la casa para que el robot la organice"]
        self.intentions: list[Plan] = []
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