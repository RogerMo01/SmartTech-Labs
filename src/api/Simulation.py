from datetime import datetime, timedelta
from House import *
from agents.bot_agent import Bot_Agent
from agents.person_agent import Person_Agent
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
        #self.person = Person_Agent(self.submmit)

        # Events list
        self.events = []


        
    def run_server(self):
        # while self.current_datetime < self.end_datetime and success == False:
        while self.end_datetime - self.current_datetime > ZERO:
            # print(self.end_datetime - self.current_datetime)
            # Take conversations in the last loop
            self.house.update_speaks()

            # Run one step in both agents
            self.bot.run(self.submmit_event)
            #self.person.run()



            # aqui supongo que se haga algo mas



            # Add one step to current_datetime
            one_step = timedelta(seconds=1)
            self.current_datetime += one_step


    def submmit_event(self, event: Event):
        self.events.append(event)

    

s = Simulation()
s.run_server()
print(s.events)


