from agents.bot_agent import *
from agents.person_agent import *

# map = []  # example map

# beliefs = {'likes': 
#          {'cinema':['thriller', 'Julia Ducournau', 'Safdie Brothers'],
#           'food': ['suschi', 'pizza']
#           },
#           'dislikes':
#           {
#             'cinema':['romantic', 'musical', 'Christopher Nolan', 'Michael Bay'],
#             'food': ['hamburguer', 'hot dog']
#           }
#           }

# beliefs = Belief(map, beliefs)
# person = Person_Agent(beliefs, Desire(), Intention())
# bot = Bot_Agent()

# def run():
#     pass


bot = Bot_Agent()
bot.run()