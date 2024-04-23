from agents.bot_agent import *
from agents.person_agent import *
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
beliefs = Bot_Belief(None, beliefs)
bot = Bot_Agent(beliefs)
bot.run()