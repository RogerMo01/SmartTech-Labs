from agents.bdi_agent import *
import random
import queue

class Bot_Belief(Belief):
    def __init__(self, map = None, beliefs = {}):
        super().__init__()
        self.last_order = None

class Bot_Agent(BDI_Agent):
    ACTIONS = [('walk',1), ('take object',2), ('charge',0), ('give recipe',1), ('cook',4), ('clean',2),('give object',1), ('recomend movie',1), ('leave object',1)] # esto no es para nada definitivo
    def __init__(self):
        super().__init__()
        
    def run(self):
        beliefs = self.beliefs
        intentions = self.intentions
        while True:  #realmente esto es simular eventos discretos y esta funcion no va aqui posiblemente
            beliefs = self.brf(beliefs)
            desire = self.options(beliefs, intentions)
            intentions = self.filter(beliefs, desire, intentions)
            plan = self.get_plan(beliefs, desire)
            while not plan.empty():
                action = plan.pop()  # this returns the function to be executed
                self.excecute(action)
                beliefs = self.brf(beliefs)
                if self.reconsider(intentions, beliefs):
                    desire = self.options(beliefs, intentions)
                    intentions = self.filter(beliefs, desire, intentions)
            
    def brf(self, beliefs):
        """Update the agent's beliefs based on the given percept.

        Args:
            percept (?): the percept of the environment
        """
        # al final esta funcion para esta simulacion no la necesitamos mucho
        # a no ser analizar cuando la persona tambien modifique el mapa.
        # ya, aqui se va a actualizar belief, que tendra un last_order
        self.beliefs = beliefs  # analizar lo de last_order de alguna manera.
        return self.beliefs
        pass

    def options(self, beliefs, intentions):
        """return the chosen desire based on the beliefs and intentions 

        Args:
            beliefs (list): all beliefs of the agent
            intentions (list): all intentions of the agent
        """
        r = random.randint(0, len(intentions)-1)  # agregar criterios para elegir deseo aquí
        return intentions[r]

    def filter(self, beliefs, desire, intentions):
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

    def reconsider(self):
        pass

    def set_plan(self):
        pass

    def get_plan(self, beliefs, desire):
        plan = queue.Empty()
        # aqui tener un switch casa para cada desire.
        pass

    def excecute(self, action):

        pass