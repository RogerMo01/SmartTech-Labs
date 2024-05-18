import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

df = pd.read_csv('src/api/stats/robot_tasks.csv')

# tiempo haciendo tareas
total_elapsed_time = df['elapsed_time'].sum()
total_elapsed_time = timedelta(seconds=total_elapsed_time)
print(f"Total-elapsed-time: {total_elapsed_time}")



########################## Daily tasks ########################
daily_tasks = dict()

all_datetimes = df['datetime']
all_days = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in all_datetimes]
all_days = list(set(all_days))
all_days = [str(d) for d in all_days]

for day in all_days:
    daily_tasks[day] = []
    for dt in all_datetimes:
        if dt.startswith(day):
            daily_tasks[day].append(dt)

daily_elapsed_time = dict()
for day in daily_tasks:
    daily_elapsed_time[day] = df[df['datetime'].str.startswith(day)]['elapsed_time'].sum()


x_dates = sorted(list(daily_elapsed_time.keys()))
y_times = [daily_elapsed_time[d] for d in x_dates]
y_times = [str(timedelta(seconds=t)) for t in y_times]

# plt.figure(figsize=(10, 5))
plt.plot(x_dates, y_times, marker='o', linestyle='-', color='g')
plt.xlabel('Día')
plt.ylabel('Tiempo')
plt.title('Tiempo diario dedicado a tareas')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



######################## Daily task times comparison ##########################
time_tasks = df[df['task_time'] > 0]
print(time_tasks)


daily_task_total_time = dict()
daily_task_time = dict()
for day in daily_tasks:
    daily_df = df[df['datetime'].str.startswith(day) & df['task_time'] > 0]
    task_times = daily_df['task_time'].tolist()
    elapsed_time = daily_df['elapsed_time'].tolist()
    postponed_time = daily_df['postponed_time'].tolist()

    print(daily_df)
    daily_task_time[day] = sum(task_times)
    daily_task_total_time[day] = sum(elapsed_time) + sum(postponed_time)

    
x_dates
y_total_task_times = [daily_task_total_time[d] for d in x_dates]
y_task_times = [daily_task_time[d] for d in x_dates]


plt.figure()
plt.plot(x_dates, y_total_task_times, label='Tiempo dedicado', marker='o', color='blue')
plt.plot(x_dates, y_task_times, label='Tiempo estimado', marker='o', color='red', linestyle=':')
plt.xlabel('Día')
plt.ylabel('Timepo(seg)')
plt.title('Comparación de tiempos')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
