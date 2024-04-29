from datetime import datetime, timedelta
from House import *
from agents.bot_agent import Bot_Agent
from agents.human_agent import Human_Agent
from event import Event

ZERO = timedelta(seconds=0)


class Simulation:
    
    def __init__(self):
        # Load initial configuration
        # with open('config.json', 'r') as f:
        #     config: dict = json.load(f)
        
        start = "2024-01-24T12:00:00.000000"
        end = "2024-01-25T12:00:00.000000"
        format = "%Y-%m-%dT%H:%M:%S.%f"
        self.start_datetime = datetime.strptime(start, format)
        self.current_datetime = self.start_datetime        
        self.end_datetime = datetime.strptime(end, format)

        self.house = House()
        other_beliefs = {
            'likes': {
                'cinema':['thriller', 'Julia Ducournau', 'Safdie Brothers'],
                'food': ['suschi', 'pizza']
                },
            'dislikes': {
                'cinema':['romantic', 'musical', 'Christopher Nolan', 'Michael Bay'],
                'food': ['hamburguer', 'hot dog']
                },
            'constraints': {}
            }

        self.bot = Bot_Agent(self.house, other_beliefs)
        self.human = Human_Agent(self.house, other_beliefs)

        # Events list
        self.events = []


        
    def run_server(self):
        # while self.current_datetime < self.end_datetime and success == False:
        while self.end_datetime - self.current_datetime > ZERO and len(self.bot.intentions) > 0:
            # print(self.end_datetime - self.current_datetime)
            # Take conversations in the last loop
            self.house.update_speaks()
            
            # Run one step in both agents
            self.bot.run(self.submmit_event)
            self.human.run(self.submmit_event)

            print(f'Will-E is: {self.bot.beliefs.bot_position}')
            print(f'Human is: {self.bot.beliefs.human_position}')
            print('.......................................')
            # aqui supongo que se haga algo mas



            # Add one step to current_datetime
            one_step = timedelta(seconds=1)
            self.current_datetime += one_step


    def submmit_event(self, event: Event):
        self.events.append(event)

    

s = Simulation()
s.run_server()
for i in s.events:
    print(i)

