import pandas as pd
from logger import *
from agents.task import Task
from agents.plan import Plan
from agents.bdi_agent import Order
import matplotlib.pyplot as plt

def save_logger(logger: Logger):
    save_robot_tasks(logger.robot_tasks)
    save_robot_plans(logger.robot_plans)
    save_preventive_recharges(logger.preventive_recharges)
    save_overtakes(logger.overtakes)
    save_understand_errors(logger.understand_errors)
    save_ignored_requests(logger.ignored_requests)

    # Show graphics


def save_robot_tasks(robot_tasks: list[TaskLog]):
    data = {
        'datetime': [],
        'type': [],
        'task_time': [],
        'elapsed_time': [],
        'postponed_time': []
    }

    for task_log in robot_tasks:
        data['datetime'].append(task_log.datetime)
        task: Task = task_log.task
        data['type'] = task.type
        data['task_time'] = task.time
        data['elapsed_time'] = task.elapsed_time
        data['postponed_time'] = task.postponed_time

    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/robot_tasks.csv', index=False)


def save_robot_plans(robot_plans: list[PlanLog]):
    data = {
        'datetime': [], 
        'intention_name': [],
        'is_postponed': [],
        'robot_boost_need': []
    }

    for plan_log in robot_plans:
        data['datetime'].append(plan_log.datetime)
        plan: Plan = plan_log.plan
        data['intention_name'].append(plan.intention_name)
        data['is_postponed'].append(plan.is_postponed)
        data['robot_boost_need'].append(plan.robot_boost_need)

    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/robot_plans.csv', index=False)



def save_preventive_recharges(preventive_recharges: list[PlanLog]):
    data = {
        'datetime': [], 
        'intention_name': [],
        'need': []
    }

    for plan_log in preventive_recharges:
        data['datetime'].append(plan_log.datetime)
        plan: Plan = plan_log.plan
        data['intention_name'].append(plan.intention_name)
        data['need'].append(plan.need)

    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/preventive_recharges.csv', index=False)


def save_overtakes(overtakes: list[OvertakeLog]):
    data = {
        'old_plan_name': [], 
        'new_plan_name': [], 
        'old_plan_need': [],
        'new_plan_need': []
    }

    for overtake in overtakes:
        data['old_plan_name'].append(overtake.old.intention_name)
        data['new_plan_name'].append(overtake.new.intention_name)
        data['old_plan_need'].append(overtake.old.robot_boost_need)
        data['new_plan_need'].append(overtake.new.robot_boost_need)
        
    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/overtakes.csv', index=False)


def save_understand_errors(understand_errors: list[Order]):
    data = {
        'order': []
    }

    for item in understand_errors:
        data['order'] = item.body
    
    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/understand_errors.csv', index=False)


def save_ignored_requests(ignored_requests: list[OrderLog]):
    data = {
        'datetime': [],
        'order': []
    }

    for item in ignored_requests:
        data['datetime'].append(item.datetime)
        data['order'].append(item.order)

    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/ignored_requests.csv', index=False)
