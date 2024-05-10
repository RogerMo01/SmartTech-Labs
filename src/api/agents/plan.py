from agents.task import *
from event import Event
from logger import logger
from agents.battery import Battery

class Plan:
    def __init__(self, intention_name, house: House, author, beliefs, tasks=[], need=None, charge_plan: bool = False):
        self.intention_name: str = intention_name      # plan name
        self.author = author
        self.house = house
        self.beliefs = beliefs
        self.tasks: list[Task] = tasks                 # list of task (type Task)
        self.is_postponed: bool = False
        self.is_successful: bool = True if len(tasks) == 0 else False
        self.need = need
        self.is_charge_plan = charge_plan

        # Log plan
        if author == "Will-E":
            logger.log_robot_plan(self)
        elif author == "Pedro":
            logger.log_human_plan(self)
        
        self.started = False

    def run(self, submmit_event, current_datetime, last_notice: Order, battery: Battery = None):
        if self.is_successful: return        # plan already finished

        
        current_task = self.tasks[0]

        if self.is_postponed or (current_task is not None and self.is_out(current_task)):
            success = self.recompute()
            if not success:
                current_task.failed = True
                current_task.is_successful = True
                self.report_task(current_task, submmit_event)

            self.is_postponed = False  
            
        current_task = self.tasks[0]

        current_task.execute(current_datetime, last_notice, battery)

        if current_task.is_successful:
            self.report_task(current_task, submmit_event)

            if len(self.tasks) == 0:
                self.is_successful = True

    def report_task(self, current_task: Task, submmit_event):
        completed = 'completed'
        failed = 'failed'
        # print(f'{self.author} {failed if current_task.failed else completed} the task ~{current_task.type}~ standing in ~{self.beliefs.bot_position.area if self.author=="Will-E" else self.beliefs.human_position.area}~ ')
        report = f'{self.author} {failed if current_task.failed else completed} the task >{current_task.type}< and now is in >{self.beliefs.bot_position.area if self.author=="Will-E" else self.beliefs.human_position.area}<'
        print(report)
        submmit_event(Event(self.author, self.intention_name, current_task))
        self.tasks.pop(0)

    def is_out(self, current_task: Task):
        """Returns false if task take place in a room or using an object and agent is not there"""

        object = current_task.object_name
        if object is not None:
            object: Object = self.house.get_object(object)
            if object.carrier is not None: return True

            current_position = self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position
            return (not current_position in object.robot_face_tiles if self.author == 'Will-E' else not current_position in object.human_face_tiles) and current_task.type != 'Caminar'      
        
        room = current_task.room
        if room is not None:
            current_area = self.beliefs.bot_position.area if self.author == 'Will-E' else self.beliefs.human_position.area
            if current_task.room is None: return False
            return (current_task.room != current_area and current_task.type != 'Caminar')
        
        return False
    

    def recompute(self):
        current_task = self.tasks[0]
        # returns tile where the object is or representative tile of area
        obj: Object = self.house.get_object(current_task.object_name)
        if obj.carrier is None:
            if self.author == "Will-E":
                dest_tile = self.house.get_tile_by_room(current_task.room) if current_task.room is not None else obj.robot_face_tiles[0]
            else:
                dest_tile = self.house.get_tile_by_room(current_task.room) if current_task.room is not None else obj.human_face_tiles[0]

            self.tasks.insert(0, Move(self.author, self.house, self.beliefs, dest_tile))
            return True
        else:
            return False

    
    def __repr__(self) -> str:
        finished = "finished"
        in_queue = "in queue"
        return f"{self.tasks.__repr__()} {finished if self.is_successful else in_queue}"
    
    def __str__(self) -> str:
        return f"({self.intention_name})"
    
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.is_successful = False


    
