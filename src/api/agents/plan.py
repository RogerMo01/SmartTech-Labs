class Plan:
    def __init__(self):
        self.tasks = []  # list of task (type Task)
        self.current_task = None
        self.is_postponed = False

    def run(self):
        self.current_task = self.tasks[0]  # esto no debe ser asi
        self.current_task.execute()
        if self.current_task.is_successful:
            self.tasks.pop(0)
        



    
