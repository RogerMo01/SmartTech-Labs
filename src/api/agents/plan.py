from agents.task import *
from event import Event

class Plan:
    def __init__(self, intention_name, house: House, author, beliefs, tasks=[]):
        self.intention_name: str = intention_name      # plan name
        self.author = author
        self.house = house
        self.beliefs = beliefs
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
            print(f'{self.author} completed the task in {self.beliefs.bot_position.area if self.author=="Will-E" else self.beliefs.human_position.area}')
            submmit_event(Event(self.author, self.intention_name, current_task))
            self.tasks.pop(0)

            if len(self.tasks) == 0:
                self.is_successful = True


    def is_out(self, current_task: Task):
        """Returns false if task take place in a room and agent is not there"""
        object = current_task.object_name
        if not object is None:
            object: Object = self.house.get_object(object)
            current_position = self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position      
            return (not current_position in object.robot_face_tiles) and current_task.type != 'Caminar'
        else:
            current_area = self.beliefs.bot_position.area if self.author == 'Will-E' else self.beliefs.human_position.area
            if current_task.room is None: return False
            return (current_task.room != current_area and current_task.type != 'Caminar')
    

    def recompute(self):
        current_task = self.tasks[0]
        # returns tile where the object is or representative tile of area
        if self.author == "Will-E":
            dest_tile = self.house.get_tile_by_room(current_task.room) if current_task.room is not None else self.house.get_object(current_task.object_name).robot_face_tiles[0]
        else:
            dest_tile = self.house.get_tile_by_room(current_task.room) if current_task.room is not None else self.house.get_object(current_task.object_name).human_face_tiles[0]


        self.tasks.insert(0, Move(self.author, self.house, self.beliefs, dest_tile))
    
    def __repr__(self) -> str:
        finished = "finished"
        in_queue = "in queue"
        return f"{self.tasks.__repr__()} {finished if self.is_successful else in_queue}"
        
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.is_successful = False


    
