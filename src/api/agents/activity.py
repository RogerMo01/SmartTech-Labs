from datetime import datetime, timedelta
from logger import logger 

class Activity:
    def __init__(self, initial_datetime: datetime) -> None:
        day = initial_datetime.day
        month = initial_datetime.month
        year = initial_datetime.year
        
        hour = initial_datetime.hour
        minute = initial_datetime.minute

        # self.all_hours = list(range(hour, 24)) + list(range(0, hour))
        self.all_hours = list(range(0, 24))
        # self.all_minutes = list(range(minute, 60)) + list(range(0, minute))
        self.all_minutes = list(range(0, 60))

        self.active_minutes = dict()

        temp_active_mins = dict()
        for hour in self.all_hours:
            for minute in self.all_minutes:
                temp_active_mins[(hour, minute)] = 0
        self.active_minutes[(day, month, year)] = temp_active_mins
        
        self.initial_datetime = initial_datetime
        self.current_date = initial_datetime
        self.best_time = (4, 0)
        logger.log_best_charging_time(self.best_time)
        
    def push(self, current_datetime: datetime):
        day = current_datetime.day
        month = current_datetime.month
        year = current_datetime.year

        hour = current_datetime.hour
        minute = current_datetime.minute

        # augment one day case
        if current_datetime.day > self.current_date.day:
            self.best_time = self.get_charge_minute()
            logger.log_best_charging_time(self.best_time)
            self.extend(day, month, year)
            self.current_date += timedelta(days=1)

        self.active_minutes[(day, month, year)][(hour, minute)] = 1



    def extend(self, day, month, year):
        active_mins = dict()
        for hour in self.all_hours:
            for minute in self.all_minutes:
                active_mins[(hour, minute)] = 0

        self.active_minutes[(day, month, year)] = active_mins


    def get_charge_minute(self):
        avg = dict()
        for hour in self.all_hours:
            for minute in self.all_minutes:
                times = 0
                acum = 0
                for day, month, year in self.active_minutes:
                    acum += self.active_minutes[(day, month, year)][(hour, minute)]
                    times += 1
                avg[(hour, minute)] = acum/times
        
        best_sum = 0
        keys = list(avg.keys())
        current_sum = 0
        first = 0
        best_index = first
        for i in range(len(keys)):
            current_sum+=avg[keys[i]]
            if i < 240:
                best_sum = current_sum
            else:
                current_sum-=avg[keys[first]]
                first +=1
                if current_sum < best_sum:
                    best_sum = current_sum
                    best_index = first
        
        return keys[best_index]
            
            