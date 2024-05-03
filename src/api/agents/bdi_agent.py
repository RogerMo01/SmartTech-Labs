from House import House
from abc import ABC
from Tile import Tile
# Belief in this case:
#   - is the information that the agent has about the world
#   - is the information that the agent has about itself
#   - is the information that the agent has about other agents

class Order:
    def __init__(self, body: str, by_human_for_need: bool):
        self.body = body
        self.by_human_for_need = by_human_for_need


class Belief:
    def __init__(self, house: House, other_beliefs = {}):
        self.map, self.objects, self.bot_position, self.human_position, self.speaks = house.get_data()
        self.likes, self.dislikes, self.constraints = self.get_belief(other_beliefs)

    def update_belief(self):
        pass

    @staticmethod
    def get_belief(beliefs):
        return beliefs['likes'], beliefs['dislikes'], beliefs['constraints']

class Perception:
    def __init__(self, map: dict, objects: dict, bot_position: Tile, human_position: Tile, speaks: list[str]):
        self.map = map
        self.objects = objects
        self.bot_position = bot_position
        self.human_position = human_position
        self.speaks = speaks

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
    # def __init__(self, beliefs, intentions = []):
    def __init__(self, beliefs):
        self.agent_id = None
        # self.map = None
        self.beliefs = beliefs
        self.desires = None
        # self.intentions = intentions
        self.intentions = None

    def see():
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

    # puede que tenga que crear otros metodos para que el agente sepa
    # cuando un plan es inviable y cosas asi




    

