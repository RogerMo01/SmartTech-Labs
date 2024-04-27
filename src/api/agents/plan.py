from agents.task import *
from event import Event

class Plan:
    def __init__(self, intention_name, author, tasks=[]):
        self.intention_name: str = intention_name      # plan name
        self.author = author
        self.tasks: list[Task] = tasks                 # list of task (type Task)
        self.is_postponed: bool = False
        self.is_successful: bool = True if len(tasks) == 0 else False


    def run(self, submmit_event):
        if self.is_successful: return        # plan already finished

        current_task = self.tasks[0]
        current_task.execute()

        if current_task.is_successful:
            print("TASK COMPLETED")
            submmit_event(Event(self.author, self.intention_name, current_task))
            self.tasks.pop(0)

            if len(self.tasks) == 0:
                self.is_successful = True
            

    def __repr__(self) -> str:
        return self.tasks.__repr__() + "--success: " + str(self.is_successful)
        



    
