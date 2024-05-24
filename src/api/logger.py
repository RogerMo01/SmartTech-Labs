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

class OrderLog:
    def __init__(self, datetime: datetime, order: Order) -> None:
        self.datetime = datetime
        self.order = order

class ConversationLog:
    def __init__(self, conversation: list[str]) -> None:
        self.conversation = conversation



class Logger:
    def __init__(self) -> None:
        self.datetime = None
        self.robot_plans: list[PlanLog] = []
        self.human_plans: list[PlanLog] = []
        self.robot_tasks: list[TaskLog] = []
        # self.human_tasks: list[TaskLog] = []
        self.overtakes: list[OvertakeLog] = []
        self.understand_errors: list[OrderLog] = []
        self.activity = None
        self.preventive_recharges: list[PlanLog] = []
        self.ignored_requests: list[OrderLog] = []
        self.conversations: list[ConversationLog] = []
        self.better_charging_times = []

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

    # def log_human_task(self, t):
    #     self.human_tasks.append(TaskLog(self.datetime, t))
    


    def log_overtake(self, old, new):
        self.overtakes.append(OvertakeLog(old, new))

    def log_understand_error(self, order: Order):
        self.understand_errors.append(OrderLog(self.datetime, order))



    def log_preventive_recharge(self, plan):
        self.preventive_recharges.append(PlanLog(self.datetime, plan))


    def log_conversation(self, conversation: list[str]):
        self.conversations.append(ConversationLog(conversation))

    def log_best_charging_time(self, time: tuple):
        self.better_charging_times.append(time)

    def log_ignored_request(self, order: Order):
        self.ignored_requests.append(OrderLog(self.datetime, order))

    def register_log(self, text: str, file_src: str):
        with open(file_src, 'a', encoding='utf-8') as file:
            text = f"[{self.datetime.strftime('%Y-%m-%d %H:%M:%S')}] {text}"
            file.write(text + '\n')



logger = Logger()