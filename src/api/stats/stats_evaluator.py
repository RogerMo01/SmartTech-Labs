import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math
import numpy as np
from matplotlib.ticker import MaxNLocator

df = pd.read_csv('src/api/stats/robot_tasks.csv')

# tiempo haciendo tareas
total_elapsed_time = df['elapsed_time'].sum()
total_elapsed_time = timedelta(seconds=total_elapsed_time)
print(f"Total-elapsed-time: {total_elapsed_time}")



######################################### Daily tasks ############################################
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


# 📒📒📒📒📒📒📒📒📒📒 Task times 📒📒📒📒📒📒📒📒📒📒
x_dates = sorted(list(daily_elapsed_time.keys()))
y_times = [daily_elapsed_time[d] for d in x_dates]
y_times = [t for t in y_times]

# plt.figure(figsize=(10, 5))
plt.plot(x_dates, y_times, marker='o', linestyle='-', color='g')
plt.xlabel('Día')
plt.ylabel('Tiempo')
plt.title('Tiempo diario dedicado a tareas')
plt.grid(True)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()








################################### Daily task times comparison ####################################
time_tasks = df[df['task_time'] > 0]

daily_task_total_time = dict()
daily_task_time = dict()
daily_postponed_task_time = dict()
for day in daily_tasks:
    daily_df = df[df['datetime'].str.startswith(day) & df['task_time'] > 0]
    task_times = daily_df['task_time'].tolist()
    elapsed_time = daily_df['elapsed_time'].tolist()
    postponed_time = daily_df['postponed_time'].tolist()

    daily_task_time[day] = sum(task_times)
    daily_postponed_task_time[day] = sum(postponed_time)
    daily_task_total_time[day] = sum(elapsed_time) + sum(postponed_time)

# ⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳ Task times statistics ⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳
x_dates
y_total_task_times = [daily_task_total_time[d] for d in x_dates]
y_task_times = [daily_task_time[d] for d in x_dates]
y_postponed_task_times = [daily_postponed_task_time[d] for d in x_dates]
y_consistency_percent = [(y_task_times[i]/y_total_task_times[i])*100 for i in range(len(y_task_times)) ]

dict_tasks = {
    "Tiempo estimado": y_task_times,
    "Tiempo total": y_total_task_times,
    "Tiempo pospuesto": y_postponed_task_times,
    r'% de eficiencia': y_consistency_percent,
}

def calculate_mean(data):
    return np.mean(data)

def calculate_variance(data):
    return np.var(data, ddof=1)

def calculate_standard_deviation(data):
    return np.std(data, ddof=1)

tasks_statistics = {}
for key, values in dict_tasks.items():
    mean = calculate_mean(values)
    var = calculate_variance(values)
    std = calculate_standard_deviation(values)
    
    tasks_statistics[key] = {
        'Media': mean, 
        'Varianza': var,
        'Desviación Estándar': std
    }

dict_tasks_df = pd.DataFrame(dict_tasks)
mean_eficiency = sum(y_consistency_percent)/len(y_consistency_percent) 
print(dict_tasks_df)
print()
print(f"Eficiencia promedio: {mean_eficiency}%")
print()

for key, stats in tasks_statistics.items():
    print(f"{key}:")
    print(f"  Media: {stats['Media']:.2f}")
    print(f"  Varianza: {stats['Varianza']:.2f}")
    print(f"  Desviación Estándar: {stats['Desviación Estándar']:.2f}")
    print()






# # Configurar la apariencia de la tabla
# styled_df = dict_tasks_df.style.background_gradient(cmap='viridis').set_properties(**{'text-align': 'center'}).set_table_styles([{
#     'selector': 'th',
#     'props': [('font-size', '12pt'), ('text-align', 'center')]
# }])

# # Convertir el DataFrame en imagen
# img = df2img.export(
#     styled_df,
#     fontsize=12,
#     table_conversion='matplotlib',
#     save_path="tabla.png"
# )







# plt.figure()
# plt.plot(x_dates, y_total_task_times, label='Tiempo dedicado', marker='o', color='blue')
# plt.plot(x_dates, y_task_times, label='Tiempo estimado', marker='o', color='red', linestyle=':')
# plt.xlabel('Día')
# plt.ylabel('Timepo(seg)')
# plt.title('Comparación de tiempos')
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.legend()
# plt.show()







################################## Charge stats #####################################
charge_tasks = df[df['type'] == 'Cargar la batería']
print(charge_tasks)

daily_charge_frecuency = dict()
for day in daily_tasks:
    daily_charge_frecuency[day] = 0

    for index, row in charge_tasks.iterrows():
        if row['datetime'] in daily_tasks[day]:
            daily_charge_frecuency[day] +=1


# 🔋🔋🔋🔋🔋🔋🔋🔋🔋🔋 Charges frequency 🔋🔋🔋🔋🔋🔋🔋🔋🔋🔋🔋
x_dates
y_frequency = [daily_charge_frecuency[d] for d in x_dates]

plt.bar(x_dates, y_frequency)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.xlabel('Día')
plt.ylabel('Frecuencia de carga')
plt.title('Histograma de frecuencias')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()





