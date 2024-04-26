from Tile import Tile
from search import *
from datetime import datetime, timedelta

ZERO = timedelta(seconds=0)

class Task:
    def __init__(self, time: timedelta):
        self.time = time         # timepo q toma en total
        self.elapsed_time = 0    # tiempo q se ha dedicado a la tarea
        self.postponed_time = 0  # timepo q lleva pospuesta
        self.is_postponed = False
        self.location = None     # lugar donde se realiza la tarea
        self.is_successful = False
    
    def execute(self, *args):
        raise Exception(NotImplemented)
    

class Move(Task):
    def __init__(self, house: House, dest: Tile):
        super().__init__(ZERO)
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.src = None
        self.dest = dest
        self.house = house
        self.steps = []

    def create_path(self, new_src=None):
        src = new_src if new_src else self.src
        p = WalkProblem(src, self.dest)
        sln = astar_search(p)
        actions = path_actions(sln)
        return actions
    
    def execute(self,*args):
        if self.elapsed_time == ZERO:
            self.src = self.house.bot_position
            self.steps = self.create_path()
            self.time = timedelta(seconds=len(self.steps))

        if self.is_postponed:
            self.steps = self.create_path(house.bot_position)  # recompute path

        direction = self.steps.pop(0) 
        self.house.move_bot(direction)
        if len(self.steps) == 0:
            self.is_successful = True



# Other types of Tasks