import pandas as pd
from logger import *
from agents.task import Task
from agents.plan import Plan
from agents.bdi_agent import Order
import matplotlib.pyplot as plt
import numpy as np

def save_logger(logger: Logger):
    save_robot_tasks(logger.robot_tasks)
    save_robot_plans(logger.robot_plans)
    save_preventive_recharges(logger.preventive_recharges)
    save_overtakes(logger.overtakes)
    save_understand_errors(logger.understand_errors)
    save_ignored_requests(logger.ignored_requests)
    save_activity(logger.activity)
    save_conversations(logger.conversations)
    
    # Save best charging time evolution
    with open('src/api/stats/better_charging_times.txt', 'w') as file:
        for t in logger.better_charging_times:
            file.write(f"{t}\n")



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
        data['type'].append(task.type)
        data['task_time'].append(task.time.total_seconds())
        data['elapsed_time'].append(task.elapsed_time.total_seconds())
        data['postponed_time'].append(task.postponed_time.total_seconds())

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


def save_understand_errors(understand_errors: list[OrderLog]):
    data = {
        'order': []
    }

    for item in understand_errors:
        data['order'] = item.order.body
    
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

def save_activity(activity):

    # (14, 2, 24)
    row_keys = list(activity.active_minutes.keys())
    # row_headers = [datetime(day=d[0], month=d[1], year=d[2]).date() for d in row_keys]
    
    # (23, 59)
    col_keys = []
    for hour in activity.all_hours:
        for minute in activity.all_minutes:
            col_keys.append((hour, minute))
    col_headers = [datetime(year=24, month=1, day=24, hour=t[0], minute=t[1], second=0).time() for t in col_keys]

    data = dict()
    for i in range(len(col_keys)):
        for row in row_keys:
            try:
                data[col_headers[i]].append(activity.active_minutes[row][col_keys[i]])
            except:
                data[col_headers[i]] = [activity.active_minutes[row][col_keys[i]]]

    df = pd.DataFrame(data)

    df.to_csv('src/api/stats/active_minutes.csv', index=False)


def save_conversations(conversations: list[ConversationLog]):
    with open("src/api/stats/conversations.txt", "a", encoding="utf-8") as file:
        for c in conversations:
            file.write("#############################################################################\n")
            for s in c.conversation:
                file.write("➡ " + s + "\n")
            file.write("\n\n\n")
            

