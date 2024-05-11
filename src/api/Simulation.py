from datetime import datetime, timedelta
from House import *
from agents.bot_agent import Bot_Agent
from agents.human_agent import Human_Agent
from event import Event
from logger import logger

ZERO = timedelta(seconds=0)
FILE_SRC = "src/api/logs/vitals.txt"

class Simulation:
    
    def __init__(self):
        # Load initial configuration
        # with open('config.json', 'r') as f:
        #     config: dict = json.load(f)
        
        start = "2024-01-24T08:00:00.000000"
        end = "2024-01-25T12:00:00.000000"
        format = "%Y-%m-%dT%H:%M:%S.%f"
        self.start_datetime = datetime.strptime(start, format)
        self.current_datetime = self.start_datetime        
        self.end_datetime = datetime.strptime(end, format)

        self.house = House()
        other_beliefs = {
            'likes':
            {
                'culinary_styles':{'mediterranean':6, 'cuban':8, 'mexican':2, 'asian':1},
                'cinema':['Star Wars', 'Lord of the Rings']
            },
            'diseases':{'diabetes':2,'heart_disease':1, 'cold':1}
            }

        self.bot = Bot_Agent(self.house, other_beliefs, self.current_datetime)
        self.human = Human_Agent(self.house, other_beliefs)

        # Events list
        self.events = []


        
    def run_server(self):
        while self.end_datetime - self.current_datetime > ZERO:
            logger.set_datetime(self.current_datetime)
            # Take conversations in the last loop
            self.house.update_speaks()

            # Run one step in both agents
            self.bot.run(self.current_datetime)
            self.human.run(self.current_datetime)
 
            d = logger.__dict__

            # Add one step to current_datetime
            one_step = timedelta(seconds=1)
            self.current_datetime += one_step

        logger
        print("END")

    def submmit_event(self, event: Event):
        self.events.append(event)

    def register_vitals(self):
        with open(FILE_SRC, 'w', encoding='utf-8') as file:
            file.write(str(self.human.needs) + '\n')
            file.write(str(self.bot.battery))

    

s = Simulation()
s.run_server()

