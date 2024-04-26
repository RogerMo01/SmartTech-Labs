from agents.bdi_agent import *
import random
import queue
from House import *
from search import *
from agents.Task import *

class Bot_Belief(Belief):
    def __init__(self, map: House = None, beliefs={}):
        super().__init__(map, beliefs)
        self.last_order = None
        

class Plan:
    def __init__(self):
        self.tasks = []

    def enqueue_task(self, task: Task):
        self.tasks.append(task)




class Bot_Agent(BDI_Agent):
    ACTIONS = ['Move to sofa', 'Move to chair1'] # for testing purposes 
    def __init__(self,beliefs, intentions = []):
        super().__init__(beliefs, intentions)
        # self.intentions:list[Plan] = []

        


    def run(self):
        self.beliefs:Bot_Belief = self.beliefs    # initial beliefs
        self.desire:Plan = self.options()   # esto es un plan

        self.desire.run()
        if self.desire.is_successful:
            print("PLAN COMPLETED")
            return True
        
        if self.reconsider():
            # reevaluate intentions
            pass
        
        return False

        


    
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
        pass

    def options(self):
        """return the chosen desire based on the beliefs and intentions 
        """
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
