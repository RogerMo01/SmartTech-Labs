from Tile import Tile
from search import *
from datetime import datetime, timedelta

ZERO = timedelta(seconds=0)

class Task:
    def __init__(self, time: timedelta):
        self.type = None
        self.time = time         # timepo q toma en total
        self.elapsed_time = 0    # tiempo q se ha dedicado a la tarea
        self.postponed_time = 0  # timepo q lleva pospuesta
        self.is_postponed = False
        self.location = None     # lugar donde se realiza la tarea
        self.is_successful = False
    
    def execute(self, *args):
        """
        Decrease 1 second of simulation completing this task.
        - must change is_successful flag
        """
        raise Exception(NotImplemented)
    

class Move(Task):
    def __init__(self, house: House, dest: Tile):
        super().__init__(ZERO)
        # self.time
        # self.postponed_time
        self.type = "Caminar"
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.src = None
        self.dest = dest
        self.house = house
        self.steps = []
        # self.is_successful

    def __repr__(self):
        return f"Move to {self.dest.name} --success: {self.is_successful}"
    
    
    def create_path(self, new_src=None):
        src = new_src if new_src else self.src
        p = WalkProblem(src, self.dest)
        sln = astar_search(p)
        actions = path_actions(sln)
        return actions
    

    def execute(self,*args):
        if self.is_successful: return                             # plan already finished

        if self.elapsed_time == ZERO:                             # initial execution
            self.recopute(timedelta(seconds=len(self.steps)))

        if self.is_postponed:
            self.recopute(self.elapsed_time + timedelta(seconds=len(self.steps)), house.bot_position)                                   # recompute path

        direction = self.steps.pop(0) 
        self.house.move_bot(direction)
        self.elapsed_time += timedelta(seconds=1)

        if len(self.steps) == 0:
            self.is_successful = True


    def recopute(self, time, new_src=None):
        self.src = self.house.bot_position
        if new_src:
            self.steps = self.create_path()
        else:
            self.steps = self.create_path(new_src)
        self.time = time
        self.is_successful = True if len(self.steps) == 0 else False

# Other types of Tasks