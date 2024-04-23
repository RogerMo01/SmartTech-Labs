from House import House
from abc import ABC
# Belief in this case:
#   - is the information that the agent has about the world
#   - is the information that the agent has about itself
#   - is the information that the agent has about other agents
class Belief:
    def __init__(self, map:House = None, beliefs = {}):
        #self.beliefs = {}
        # i can add something like string-array tuple to store the beliefs
        self.map = map
        self.likes, self.dislikes, self.constraints = self.get_belief(beliefs)

    def update_belief(self):  # this is not clear for me
        pass

    @staticmethod
    def get_belief(beliefs):
        return beliefs['likes'], beliefs['dislikes'], beliefs['constraints']
    

 # -------------------------        
 # I DON'T NEED THIS SECTION
 # -------------------------
class Desire: # this is the goal that the agent wants to achieve
    def __init__(self):
        self.desires = []
        
class Intention:  # this is the plan that the agent has to achieve its desires
    def __init__(self):
        self.intentions = []  

    def add_intention(self, action):
        self.intentions.append(action)
    
    def clear_intentions(self):
        self.intentions = []
# -------------------------
# I DON'T NEED THIS SECTION
# -------------------------


class BDI_Agent(ABC):
    def __init__(self, beliefs, desires = [], intentions = []):
        self.agent_id = None
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions

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

    # puede que tenga que crear otros metodos para que el agente sepa
    # cuando un plan es inviable y cosas asi




    

