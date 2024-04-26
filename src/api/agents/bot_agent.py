from agents.bdi_agent import *
import random
import queue
from House import *
from search import *
from task import *

class Bot_Belief(Belief):
    def __init__(self, map: House = None, beliefs={}):
        super().__init__(map, beliefs)
        self.last_order = None
        self.map = House()

class Plan:
    def __init__(self):
        self.tasks = []

    def enqueue_task(self, task: Task):
        self.tasks.append(task)




class Bot_Agent(BDI_Agent):
    ACTIONS = ['Move to sofa', 'Move to chair1'] # for testing purposes 
    def __init__(self,beliefs,desires = [], intentions = []):
        super().__init__(beliefs,desires, intentions)
        self.intentions = ['Move to sofa']

        self.plans = []

        
    
    def run(self):  # for now, i'll use beliefs from self
        
        #beliefs = self.beliefs  commented, for now
        intentions = self.intentions
        
        while True:
            #beliefs = self.brf(beliefs)
            desire = self.options(self.beliefs, self.intentions)
            intentions = self.filter(self.beliefs, desire, self.intentions)
            plan = self.get_plan(self.beliefs, desire)
            while not plan.empty():
                action = plan.get()  # this returns the function to be executed
                self.execute(action)
                if self.reconsider(intentions, self.beliefs):
                    desire = self.options(self.beliefs, intentions)
                    intentions = self.filter(self.beliefs, desire, intentions)
            self.intentions.remove(desire)
            if len(self.intentions) == 0:
                break
    
            
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
        #r = random.randint(0, len(intentions)-1)  # agregar criterios para elegir deseo aquí
        r = 0
        return intentions[r]

    def filter(self, beliefs, desire, intentions):  # i'll use this method later
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

    def reconsider(self, intentions, general_beliefs):
        # if self.beliefs == general_beliefs i should do something like this
        return False

    def get_plan(self, beliefs, desire):  # i dont use beliefs here and i think i dont need to.
        plan = queue.Queue()
        if desire == 'Move to sofa':
            moves = self.move_to_sofa()
            for m in moves:
                plan.put((self.walk,m))  # no me queda claro que sea la mejor manera
        elif desire == 'Move to chair1':
            plan.put(self.ACTIONS[1])  # parche analogo.
        return plan

    def execute(self, action):
        function = action[0]
        arg = action[1]  # for now, the action walk only needs the direction
        function(arg)


    def walk(self, direction):  # i dont know how to manage the beliefs here
        current = self.beliefs.map.bot_position
        if direction == UP:
            self.beliefs.map.bot_position = current.up
        elif direction == DOWN:
            self.beliefs.map.bot_position = current.down
        elif direction == LEFT:
            self.beliefs.map.bot_position = current.left
        elif direction == RIGHT:
            self.beliefs.map.bot_position = current.right
        else:
            raise ValueError('Invalid direction')
        
    # ---------------------
    # FOR TESTING PURPOSES
    # ---------------------
    def move_to_sofa(self):
         current_position = self.beliefs.map.bot_position
         p = WalkProblem(current_position, H9)  # H9 is the sofa
         sln = astar_search(p)
         actions = path_actions(sln)
         return actions
    
    def move_to_chair1(self):
        current_position = self.beliefs.map.bot_position
        p = WalkProblem(current_position, H11)  # H11 is the chair1
        sln = astar_search(p)
        actions = path_actions(sln)
        return actions
