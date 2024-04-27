from datetime import datetime, timedelta
from agents.task import Task

class Event:
    def __init__(self, author: str, intention: str, task: Task):
        self.author = author
        self.intention = intention
        self.task = task

    def __str__(self) -> str:
        return f"{self.author} completó: tarea de tipo ({self.task.type}) en el tiempo ({self.task.elapsed_time}) como parte del plan ({self.intention})"
    
    def __repr__(self) -> str:
        return self.__str__()