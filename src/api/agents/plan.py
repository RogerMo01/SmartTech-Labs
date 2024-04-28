from agents.task import *
from event import Event

class Plan:
    def __init__(self, intention_name, house: House, author, tasks=[]):
        self.intention_name: str = intention_name      # plan name
        self.author = author
        self.house = house
        self.tasks: list[Task] = tasks                 # list of task (type Task)
        self.is_postponed: bool = False
        self.is_successful: bool = True if len(tasks) == 0 else False
        

    def run(self, submmit_event):
        if self.is_successful: return        # plan already finished

        
        current_task = self.tasks[0]
        
        if self.is_postponed or self.is_out(current_task):
            self.recompute()
            self.is_postponed = False  
            
        current_task = self.tasks[0]

        current_task.execute()

        if current_task.is_successful:
            print("TASK COMPLETED")
            submmit_event(Event(self.author, self.intention_name, current_task))
            self.tasks.pop(0)

            if len(self.tasks) == 0:
                self.is_successful = True


    def is_out(self, current_task):
        current_area = self.house.bot_position.area if self.author == 'Bot' else self.house.human_position.area
        return (current_task.room != current_area and current_task.type != 'Caminar')
    

    def recompute(self):
        current_task = self.tasks[0]
        dest_tile = self.house.get_tile_by_room(current_task.room)
        current_area = self.house.bot_position.area if self.author == 'Bot' else self.house.human_position.area

        if not current_task.room == current_area:
            self.tasks.insert(0, Move(self.author, self.house, dest_tile))
    
    def __repr__(self) -> str:
        return self.tasks.__repr__() + "--success: " + str(self.is_successful)
        



    
