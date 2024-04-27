from agents.bdi_agent import *
import random
import queue
from House import *
from search import *
from agents.task import *
from agents.plan import *

class Bot_Belief(Belief):
    def __init__(self, house: House = None, other_beliefs={}):
        super().__init__(house, other_beliefs)
        self.last_order = None
        # self.map
        # self.likes
        # self.dislikes
        # self.constraints
        


class Bot_Agent(BDI_Agent):
    ACTIONS = ['Move to sofa', 'Move to chair1'] # for testing purposes 

    def __init__(self, house: House, other_beliefs: dict):
        # super().__init__(beliefs, intentions)
        self.agent_id = 'Bot'
        self.beliefs = Bot_Belief(house, other_beliefs) # initial beliefs
        self.desires = ["Ayudar al humano en todo lo que pueda, en el hogar"]
        self.intentions: list[Plan] = [Plan("Ir al sofa", self.agent_id, [Move(house, E8)])]


    def run(self, submmit_event):
        # Percibir lo nuevo del entorno
        # en base a las percepciones actualizar mis creencias y actualizar mi lista de intenciones (considerar)
        # (actualmente como no se percibe nada nuevo, no es necesario esto)

        # perceptions = self.percept()
        # self.beliefs = self.brf(perceptions)

        # Plans already in queue
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
        

        
    def percept(self):
        """Percepts changes in enviroment"""
        return None

    
    # def run(self):  # for now, i'll use beliefs from self
        
    #     beliefs = self.beliefs  
    #     intentions = self.intentions
        
        
    #     while True:
    #         #beliefs = self.brf(beliefs)
    #         desire = self.options(self.beliefs, self.intentions)
    #         intentions = self.filter(self.beliefs, desire, self.intentions)
    #         plan = self.get_plan(self.beliefs, desire)
    #         while not plan.empty():
    #             action = plan.get()  # this returns the function to be executed
    #             self.execute(action)
    #             if self.reconsider(intentions, self.beliefs):
    #                 desire = self.options(self.beliefs, intentions)
    #                 intentions = self.filter(self.beliefs, desire, intentions)
    #         self.intentions.remove(desire)
    #         if len(self.intentions) == 0:
    #             break
    
            
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

    def options(self):
        """Return the chosen desire based on the beliefs and intentions"""
        #r = random.randint(0, len(intentions)-1)  # agregar criterios para elegir deseo aquí
        r = 0
        return self.intentions[r]

    # def filter(self, beliefs, desire, intentions):  # i'll use this method later
    #     """return the filtered intentions based on the beliefs and selected desire

    #     Args:
    #         beliefs (list): all beliefs of the agent
    #         desire (str): chosen desire
    #         intentions (list): all intentions of the agent
    #     """
    #     for i in intentions:
    #         if i == desire:
    #             return i
    #     pass

    def reconsider(self):
        # if self.beliefs == general_beliefs i should do something like this
        return False
