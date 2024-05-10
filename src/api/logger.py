from datetime import *
from agents.bdi_agent import Order


class PlanLog:
    def __init__(self, datetime: datetime, plan) -> None:
        self.datetime = datetime
        self.plan = plan
    def __repr__(self) -> str:
        return self.plan.intention_name
    
class TaskLog:
    def __init__(self, datetime: datetime, task) -> None:
        self.datetime = datetime
        self.task = task
    def __repr__(self) -> str:
        return self.task.type

class OvertakeLog:
    def __init__(self, old, new) -> None:
        self.old = old
        self.new = new



class Logger:
    def __init__(self) -> None:
        self.datetime = None
        self.robot_plans: list[PlanLog] = []
        self.human_plans: list[PlanLog] = []
        self.robot_tasks: list[TaskLog] = []
        self.human_tasks: list[TaskLog] = []
        self.overtakes: list[OvertakeLog] = []
        self.understand_errors: list[Order] = []

    def set_datetime(self, datetime: datetime):
        self.datetime = datetime



    def log_robot_plan(self, p):
        self.register_log(f"Will-E planifica >{p.intention_name}", "src/api/logs/will-e.txt")
        self.robot_plans.append(PlanLog(self.datetime, p))

    def log_human_plan(self, p):
        self.register_log(f"Pedro planifica >{p.intention_name}", "src/api/logs/pedro.txt")
        self.human_plans.append(PlanLog(self.datetime, p))

    def log_robot_task(self, t):
        self.robot_tasks.append(TaskLog(self.datetime, t))

    def log_human_task(self, t):
        self.human_tasks.append(TaskLog(self.datetime, t))



    def log_overtake(self, old, new):
        self.overtakes.append(OvertakeLog(old, new))

    def log_understand_error(self, order: Order):
        self.understand_errors.append(order)



    def register_log(self, text: str, file_src: str):
        with open(file_src, 'a', encoding='utf-8') as file:
            text = f"[{self.datetime.strftime('%Y-%m-%d %H:%M:%S')}] {text}"
            file.write(text + '\n')



logger = Logger()