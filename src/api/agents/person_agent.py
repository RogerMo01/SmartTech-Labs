from agents.bdi_agent import *

class Person_Agent(BDI_Agent):
    def __init__(self):
        super().__init__()
        self.beliefs = Belief()
        self.desires = Desire()
        self.intentions = Intention()
        self.plan = [] # list of actions

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