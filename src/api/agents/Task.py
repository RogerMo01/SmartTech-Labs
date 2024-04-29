from Tile import Tile
from search import *
from agents.bdi_agent import Belief
from datetime import datetime, timedelta

ZERO = timedelta(seconds=0)

class Task:
    def __init__(self, author, time: timedelta, room: str = None, house: House=None, beliefs: Belief = None, is_priority: bool = False):
        self.type = None
        self.author = author
        self.time = time         # timepo q toma en total
        self.room = room
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.postponed_time = ZERO  # timepo q lleva pospuesta
        self.is_postponed = False
        self.location = None     # lugar donde se realiza la tarea
        self.is_successful = False
        self.house = house
        self.beliefs = beliefs
        self.is_priority = is_priority

    def execute(self, *args):
        """
        Decrease 1 second of simulation completing this task.
        - must change is_successful flag
        """
        raise Exception(NotImplemented)
    

class Move(Task):
    def __init__(self, author, house: House, beliefs: Belief, dest: Tile):
        super().__init__(author, ZERO)
        # self.time
        # self.postponed_time
        self.type = "Caminar"
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.src = None
        self.dest = dest
        self.house = house
        self.steps = []
        self.beliefs = beliefs
        # self.is_successful

    def __repr__(self):
        return f"Move to {self.dest.name} --success: {self.is_successful}"
    
    
    def create_path(self, new_src=None):
        src = new_src if new_src else self.src
        p = WalkProblem(src, self.dest)
        sln = astar_search(p)
        actions = path_actions(sln)
        return actions
    

    def execute(self, *args):
        if self.is_successful: return                             # plan already finished

        if self.elapsed_time == ZERO:                             # initial execution
            self.recompute(timedelta(seconds=len(self.steps)))

        if self.is_postponed:
            self.recompute(self.elapsed_time + timedelta(seconds=len(self.steps)), 
                           self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position)                                    # recompute path

        direction = self.steps.pop(0) 
        new_pos = self.house.move(direction, self.author)
        self.beliefs.bot_position = new_pos
        self.elapsed_time += timedelta(seconds=1)

        if len(self.steps) == 0:
            self.is_successful = True


    def recompute(self, time, new_src=None):
        self.src = self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position
        if new_src:
            self.steps = self.create_path()
        else:
            self.steps = self.create_path(new_src)
        self.time = time
        self.is_successful = True if len(self.steps) == 0 else False

class Clean(Task):
    def __init__(self, author, house: House, beliefs: list[Belief], room: str):
        super().__init__(author, ZERO)
        self.time = timedelta(seconds=5)
        self.type = "Limpiar"
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.room = room
        self.house = house
        self.is_successful
        self.beliefs = beliefs

    def __repr__(self):
        return f"Clean {self.tile.name} --success: {self.is_successful}"
    
    def execute(self, *args):
        if self.is_successful: return                             
        
        print(f'Cleaning... {self.elapsed_time}')
        
        self.elapsed_time += timedelta(seconds=1)

        if self.elapsed_time == self.time:
            self.is_successful = True

    