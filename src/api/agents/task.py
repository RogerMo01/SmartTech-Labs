import json
from Tile import Tile
from search import House
from search import *
from agents.bdi_agent import Belief, Order
from datetime import datetime, timedelta
from agents.needs import Needs
from llm.prompts import human_conversation_prompt, robot_conversation_prompt, recipe_constructor_prompt
from simulation_data import BEST_TIMES, CONSUMPTION_PER_TASK
from llm.gemini import Gemini
from agents.sentence import *
from agents.recommenders import call_recommenders
from agents.battery import Battery

ZERO = timedelta(seconds=0)

class Task:
    def __init__(self, author, time: timedelta, room: str = None, house: House=None, beliefs: Belief = None, is_priority: bool = False, object_name: str = None):
        self.type = None
        self.author = author
        self.time = time         # timepo q toma en total
        self.room = room
        self.object_name = object_name     
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.postponed_time = ZERO  # timepo q lleva pospuesta
        self.is_postponed = False
        self.is_successful = False
        self.house = house
        self.beliefs = beliefs
        self.is_priority = is_priority
        self.failed = False

    
    def __repr__(self):
        finished = "finished"
        in_queue = "in queue"
        if self.room:
            return f"{self.type} in {self.room} - {finished if self.is_successful else in_queue}"
        else:
            return f"{self.type} {finished if self.is_successful else in_queue}"

    def execute(self, current_datetime: datetime, *args):
        """
        Decrease 1 second of simulation completing this task.
        - must change is_successful flag
        """
        raise Exception(NotImplemented)
    

class Move(Task):
    def __init__(self, author, house: House, beliefs: Belief, dest: Tile):
        super().__init__(author, ZERO)
        # self.time
        # self.postponed_time
        self.type = "Caminar"
        self.elapsed_time = ZERO    # tiempo q se ha dedicado a la tarea
        self.src = None
        self.dest = dest
        self.house = house
        self.steps = []
        self.beliefs = beliefs
        # self.is_successful

    def __repr__(self):
        finished = "finished"
        in_queue = "in queue"
        return f"Move to {self.dest.name} {finished if self.is_successful else in_queue}"
    
    
    def create_path(self, new_src=None):
        src = new_src if new_src else self.src
        p = WalkProblem(src, self.dest, agent = 'bot' if self.author == "Will-E" else 'human')
        sln = astar_search(p)
        actions = path_actions(sln)
        return actions
    

    def execute(self, current_datetime: datetime, order: Order, battery: Battery = None, *args):
        if self.is_successful: return                             # plan already finished

        if self.elapsed_time == ZERO:                             # initial execution
            self.recompute(timedelta(seconds=len(self.steps)))

        if self.is_postponed:
            self.recompute(self.elapsed_time + timedelta(seconds=len(self.steps)), 
                           self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position)                                    # recompute path

        if len(self.steps) != 0:
            direction = self.steps.pop(0) 
            self.house.move(direction, self.author)
                
        self.elapsed_time += timedelta(seconds=1)

        if self.author == 'Will-E':
            battery.decrease_battery(CONSUMPTION_PER_TASK["move_speak"])

        if len(self.steps) == 0:
            self.is_successful = True


    def recompute(self, time, new_src=None):
        self.src = self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position
        if new_src:
            self.steps = self.create_path(new_src)
        else:
            self.steps = self.create_path()
        self.time = time
        self.is_successful = True if len(self.steps) == 0 else False

class TimeTask(Task):
    def __init__(self, author, house: House, beliefs: list[Belief], time: timedelta, room: str = None, object: str = None, type=None):
        super().__init__(author, time, room, house, beliefs, object_name=object)
        self.type = type
        # self.is_successful
    
    def execute(self, current_datetime: datetime, order: Order, battery: Battery, *args):
        if self.is_successful: return                             
        
        self.elapsed_time += timedelta(seconds=1)

        battery.decrease_battery(CONSUMPTION_PER_TASK["time_task"])

        if self.elapsed_time == self.time:
            self.is_successful = True

class Clean(TimeTask):
    def __init__(self, author, house: House, beliefs: list[Belief], time: timedelta, room: str = None, object: str = None):
        super().__init__(author, house, beliefs, time, room, object, 'Limpiar')

class UseWater(TimeTask):
    def __init__(self, author, house: House, beliefs: list[Belief], time: timedelta, room: str = None, object: str = None):
        super().__init__(author, house, beliefs, time, room, object, "Echar agua")
    

class Take(Task):
    def __init__(self, author: str, obj: Object, house: House, pocket: list):
        super().__init__(author, timedelta(seconds=1), house=house, object_name=obj.name)
        self.type = "Coger"
        self.obj = obj
        self.pocket = pocket

    def __repr__(self):
        finished = "finished"
        in_queue = "in queue"
        return f"{self.type} {self.obj.name} {finished if self.is_successful else in_queue}"

    def execute(self, current_datetime: datetime, order: Order, battery: Battery, *args):
        if self.is_successful: return     
        
        # Hacer las acciones para coger el objeto
        if self.obj.carrier is None:
            self.house.take_object(self.author, self.obj)
            self.pocket.append(self.obj)
        else:
            self.failed = True

        self.elapsed_time += timedelta(seconds=1)

        battery.decrease_battery(CONSUMPTION_PER_TASK["take_drop"])

        if self.elapsed_time == self.time:
            self.is_successful = True


class Drop(Task):
    def __init__(self, author: str, obj: Object, house: House, pocket: list):
        super().__init__(author, timedelta(seconds=1), house=house, object_name=obj.name)
        self.type = "Soltar"
        self.obj = obj
        self.pocket = pocket

    def __repr__(self):
        finished = "finished"
        in_queue = "in queue"
        return f"{self.type} {self.obj.name} {finished if self.is_successful else in_queue}"

    def execute(self, current_datetime: datetime, order: Order, battery: Battery, *args):
        if self.is_successful: return     
        
        # Hacer las acciones para soltar el objeto 
        self.house.drop_object(self.author, self.obj)
        self.pocket.remove(self.obj)
        
        self.elapsed_time += timedelta(seconds=1)

        battery.decrease_battery(CONSUMPTION_PER_TASK["take_drop"])

        if self.elapsed_time == self.time:
            self.is_successful = True


class PlayMusic(Task):
    def __init__(self, author, time: timedelta, room: str = None, house: House = None, is_priority: bool = False):
        super().__init__(author, time, room, house, None, is_priority, None)

    def execute(self, current_datetime: datetime, order: Order, battery: Battery, *args):
        if self.is_successful: return 

        if not self.house.get_is_music_playing():
            self.house.set_is_music_playing(True)

        self.elapsed_time += timedelta(seconds=1)

        battery.decrease_battery(CONSUMPTION_PER_TASK["play_music"])

        if self.elapsed_time == self.time:
            self.house.set_is_music_playing(False)
            self.is_successful = True

# class StopMusic(Task):
#     def __init__(self, author, time: timedelta, room: str = None, house: House = None, is_priority: bool = True):
#         super().__init__(author, time, room, house, None, is_priority, None)
#         self.time = 1

#     def execute(self, current_datetime: datetime, *args):
#         if self.is_successful: return 

#         if not self.house.get_is_music_playing():
#             self.house.set_is_music_playing(False)

#         self.elapsed_time += timedelta(seconds=1)

#         if self.elapsed_time == self.time:
#             self.is_successful = True

class Charge(Task):
    def __init__(self, author, house: House = None, beliefs: Belief = None, object_name: str = None):
        super().__init__(author, ZERO, None, house, beliefs, False, object_name)

    def execute(self, current_datetime: datetime, order, battery: Battery, *args):
        if self.is_successful: return     
        
        battery.increase_battery()

        self.elapsed_time += timedelta(seconds=1)

        if battery.percent_battery == 100:
            self.is_successful = True


class Need(Task):
    def __init__(self, author, time: timedelta, type: str, house: House = None, beliefs: Belief = None, object_name: str = None, need: str = None, needs: Needs = None):
        super().__init__(author, time, None, house, beliefs, object_name=object_name)
        self.type = type
        self.needs = needs
        self.need = need
        self.inc = 100/BEST_TIMES[self.need]
        # Para incremento infimo en funcion del tiempo, subir entre 5 y 10
        if time.seconds * self.inc < 5:
            self.inc = random.randint(5, 8)/time.seconds

    def execute(self, current_datetime: datetime, *args):
        if self.is_successful: return     

        self.needs.sum_level(self.need, self.inc)
        
        self.elapsed_time += timedelta(seconds=1)

        if self.elapsed_time == self.time or self.needs[self.need] > 99:
            self.is_successful = True
        pass



class Sleep(TimeTask):
    def __init__(self, author, house: House, beliefs: list[Belief], room: str = None, object: str = None):
        super().__init__(author, house, beliefs, timedelta(seconds=15), room, object, "Dormir")



class Speak(Task):
    def __init__(self, author, listener, last_notice, house: House = None, beliefs: Belief = None, message: str = None, human_need: bool = False):
        super().__init__(author, ZERO, None, house, beliefs)
        self.listener = listener
        self.start_message = message
        self.human_need = human_need
        self.last_notice = last_notice
        self.conversation = []
        self.my_turn = True
        self.type = f"Hablar a {self.listener}"
        # self.my_turn = True if message is not None else False
        self.llm = Gemini()
        self.requested_recipe = False

    def execute(self, current_datetime: datetime, last_notice: Order, battery: Battery = None, *args):
        if self.is_successful: return    

        if self.my_turn:
            
            if last_notice is None :
                # Listener did't speak and I am not starter
                if len(self.conversation) > 0:
                    self.is_successful = True
                    return
            # Listener sayed something
            else:
                # Update with last_notice
                self.conversation.append(Sentence(self.listener, last_notice.body))


            # Start conversation case
            if len(self.conversation) == 0:
                response = self.start_message
            # Reply case
            else:
                conversation_prompt = robot_conversation_prompt(self.conversation) if self.author == "Will-E" else human_conversation_prompt(self.conversation)
                
                # Try get response 3 times
                tries = 0
                while tries < 3:
                    try:
                        out = self.llm(conversation_prompt)
                        out = json.loads(out)
                        response = out["response"]
                        tries = 3
                    except:
                        tries+=1
                    

                if response == "END":
                    self.is_successful = True
                    return
                
                # Use customized response for recipe
                if self.author == "Will-E":
                    try:
                        recipe_query = out["comida"] == "SI"
                        if not self.requested_recipe and recipe_query:
                            self.requested_recipe = True
                            #######################################################
                            culinary_styles, diseases = self.beliefs.get_data_for_recommender()
                            recommend_dish = call_recommenders(diseases, culinary_styles, current_datetime.hour)
                            # Prompt para recomendar receta con el sistema experto
                            recipe_prompt = recipe_constructor_prompt(self.conversation, recommend_dish)
                            response = self.llm(recipe_prompt)
                            #######################################################
                    except:
                        # Take as no recipe
                        pass
                

            self.house.say(self.author, response, by_human_for_need=self.human_need)
            self.conversation.append(Sentence(self.author, response))

            # Wait 1 loop
            self.my_turn = False
        
        # Not my turn
        else:
            # waiting...
            self.my_turn = True
        
        self.elapsed_time += timedelta(seconds=1)
        self.time += timedelta(seconds=1)

        if self.author == "Will-E":
            battery.decrease_battery(CONSUMPTION_PER_TASK["move_speak"])