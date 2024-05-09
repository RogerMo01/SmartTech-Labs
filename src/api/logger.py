from datetime import *
from agents.bdi_agent import Order


class PlanLog:
    def __init__(self, datetime: datetime, plan) -> None:
        self.datetime = datetime
        self.plan = plan
    def __repr__(self) -> str:
        return self.plan.intention_name

class OvertakeLog:
    def __init__(self, old, new) -> None:
        self.old = old
        self.new = new



class Logger:
    def __init__(self) -> None:
        self.datetime = None
        self.robot_plans: list[PlanLog] = []
        self.human_plans: list[PlanLog] = []
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


    def log_overtake(self, old, new):
        self.overtakes.append(OvertakeLog(old, new))

    def log_understand_error(self, order: Order):
        self.understand_errors.append(order)




    def register_log(self, text: str, file_src: str):
        with open(file_src, 'a', encoding='utf-8') as file:
            text = f"[{self.datetime.strftime('%Y-%m-%d %H:%M:%S')}] {text}"
            file.write(text + '\n')



logger = Logger()