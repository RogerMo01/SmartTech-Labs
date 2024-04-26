class Plan:
    def __init__(self):
        self.tasks = []  # list of task (type Task)
        self.current_task = None
        self.is_postponed = False
        self.is_successful = False
        self.intention = None   # nombre del plan

    def run(self):
        self.current_task = self.tasks[0]  # esto no debe ser asi
        self.current_task.execute()
        if self.current_task.is_successful:
            print("TASK COMPLETED")
            self.tasks.pop(0)
            if len(self.tasks) == 0:
                self.is_successful = True # fin del plan

    def __repr__(self) -> str:
        return self.tasks.__repr__() + "--success: " + str(self.is_successful)
        



    
