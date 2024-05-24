from agents.activity import Activity
from datetime import datetime, timedelta
import pandas as pd

SELECTOR = 8
head_path = f'src/api/tests/sim{SELECTOR}/'

start = "2024-01-10T00:00:00.000000"
format = "%Y-%m-%dT%H:%M:%S.%f"
start_datetime = datetime.strptime(start, format)
current_datetime = start_datetime
act = Activity(start_datetime)


activity_df = pd.read_csv(head_path + 'active_minutes.csv')

for index, row in activity_df.iterrows():
    print(f"Fila {index}:")

    for column, value in row.items():
        if value == 1:
            act.push(current_datetime)
        current_datetime += timedelta(minutes=1)

print("END")