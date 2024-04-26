from agents.plan import *
from agents.task import *
from House import House

# from agents.bot_agent import *
# from agents.person_agent import *
# beliefs = {'likes': 
#          {'cinema':['thriller', 'Julia Ducournau', 'Safdie Brothers'],
#           'food': ['suschi', 'pizza']
#           },
#           'dislikes':
#           {
#             'cinema':['romantic', 'musical', 'Christopher Nolan', 'Michael Bay'],
#             'food': ['hamburguer', 'hot dog']
#           },
#           'constraints':
#           {}
#           }
# beliefs = Bot_Belief(None, beliefs)
# bot = Bot_Agent(beliefs)
# bot.run()
h = House()
p = Plan()
print(h.bot_position)
print('..........................')
p.tasks = [Move(0,h,h.bot_position, H9), Move(0,h,H9,G9),Move(0,h,G9,E9)]
for i in p.tasks:
    while not i.is_successful:
        p.run()
        print('..........................')
        print(h.bot_position)


