import json
import threading
from queue import Queue
import datetime
from House import House
# from agents.bot_agent import Bot_Agent
# from agents.person_agent import Person_Agent


class Bot_Agent:
    pass
class Person_Agent:
    pass


class Event:
    def __init__(self, description: str, start_time: datetime.datetime, lapse: datetime.timedelta):
        self.description = description
        self.time = start_time
        self.lapse = lapse


class Simulation:
    def __init__(self):
        # Load initial configuration
        with open('archivo.json', 'r') as f:
            config: dict = json.load(f)
        
        self.start_datetime = config['start_datetime']
        self.current_datetime = self.start_datetime
        self.end_datetime = config['end_datetime']

        self.house = House()

        # se le debe pasar info
        self.bot = Bot_Agent(self.submmit)
        self.person = Person_Agent(self.submmit)

        # Events list
        self.events = []


        
    def run_server(self):
        while self.end_datetime - self.current_datetime > 0:

            # Take conversations in the last loop
            self.house.update_speaks()

            # Run one step in both agents
            self.bot.run()
            self.person.run()



            # aqui supongo que se haga algo mas



            # Add one step to current_datetime
            one_step = datetime.timedelta(seconds=1)
            self.current_datetime += one_step




    def submmit_event(self, event: Event):
        self.events.append(event)