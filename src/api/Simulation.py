import json
import threading
from queue import Queue
import datetime
from House import *
from agents.bot_agent import Bot_Agent
from agents.person_agent import Person_Agent
from agents.bdi_agent import Belief
from agents.plan import Plan
from agents.Task import Move

class Event:
    def __init__(self, description: str, start_time: datetime.datetime, lapse: datetime.timedelta):
        self.description = description
        self.time = start_time
        self.lapse = lapse


class Simulation:
    
    def __init__(self):
        # Load initial configuration
        # with open('archivo.json', 'r') as f:
        #     config: dict = json.load(f)
        
        # self.start_datetime = config['start_datetime']
        # self.current_datetime = self.start_datetime
        # self.end_datetime = config['end_datetime']
        self.start_datetime = 0
        self.current_datetime = 0  
        self.end_datetime = 10

        self.house = House()
        beliefs = {'likes': 
         {'cinema':['thriller', 'Julia Ducournau', 'Safdie Brothers'],
          'food': ['suschi', 'pizza']
          },
          'dislikes':
          {
            'cinema':['romantic', 'musical', 'Christopher Nolan', 'Michael Bay'],
            'food': ['hamburguer', 'hot dog']
          },
          'constraints':
          {}
          }

        beliefs = Belief(self.house, beliefs)
        # se le debe pasar info
        #self.bot = Bot_Agent(self.submmit)
        p = Plan()
        p.tasks = [Move(self.house, H9), Move(self.house,G9),Move(self.house,E9)]
        self.bot = Bot_Agent(beliefs,[p])
        #self.person = Person_Agent(self.submmit)

        # Events list
        self.events = []


        
    def run_server(self):
        x = 0
        # while self.end_datetime - self.current_datetime > 0:
        success = False
        while self.current_datetime < self.end_datetime and success == False:
            # Take conversations in the last loop
            #self.house.update_speaks()

            # Run one step in both agents
            success = self.bot.run()
            #self.person.run()



            # aqui supongo que se haga algo mas



            # Add one step to current_datetime
            # one_step = datetime.timedelta(seconds=1)
            self.current_datetime += 1
            print(self.current_datetime)




    def submmit_event(self, event: Event):
        self.events.append(event)

    



s = Simulation()
s.run_server()



