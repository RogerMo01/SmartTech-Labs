from agents.task import *
from logger import logger
from agents.battery import Battery
import simulation_data

class Plan:
    def __init__(self, intention_name, house: House, author, beliefs, tasks, need=None, charge_plan: bool = False, robot_boost_need: bool = False):
        self.intention_name: str = intention_name      # plan name
        self.author = author
        self.house = house
        self.beliefs = beliefs
        self.tasks: list[Task] = tasks                 # list of task (type Task)
        self.is_postponed: bool = False
        self.is_successful: bool = True if len(tasks) == 0 else False
        self.need = need
        self.is_charge_plan = charge_plan
        self.robot_boost_need = robot_boost_need

        # Log plan
        if author == "Will-E":
            logger.log_robot_plan(self)
        elif author == "Pedro":
            logger.log_human_plan(self)
        
        self.started = False

    def run(self, current_datetime, last_notice: Order, battery: Battery = None, understand_func = None):
        if self.is_successful: return        # plan already finished

        if len(self.tasks) == 0:
            self.is_successful = True
            return
        
        current_task = self.tasks[0]

        if self._get_is_postponed(current_task) and (current_task is not None and self.is_out(current_task)):
            success = self.recompute()
            if not success:  # if carrier is not None only
                current_task.failed = True
                current_task.is_successful = True
                self.tasks.pop(0)
        elif self._get_is_postponed_without_object(current_task):
            self.is_postponed = False

        current_task = self.tasks[0]

        current_task.execute(current_datetime, last_notice, battery, understand_func)

        if current_task.is_successful:
            self.tasks.pop(0)

            if len(self.tasks) == 0:
                self.is_successful = True

    def _get_is_postponed(self, current_task: Task):
        return self.is_postponed and (current_task.object_name is not None or current_task.room is not None)
    
    def _get_is_postponed_without_object(self, current_task: Task):
        return self.is_postponed and (current_task.object_name is None and current_task.room is None)
    
    def is_out(self, current_task: Task):
        """Returns false if task take place in a room or using an object and agent is not there"""

        object = current_task.object_name
        room = current_task.room
        if object is not None:
            object: Object = self.house.get_object(object)
            if object.carrier is not None: return True

            current_position = self.beliefs.bot_position if self.author == 'Will-E' else self.beliefs.human_position
            return (not current_position in object.robot_face_tiles if self.author == 'Will-E' else not current_position in object.human_face_tiles) and current_task.type != 'Caminar'      
       
        elif room is not None:
            current_area = self.beliefs.bot_position.area if self.author == 'Will-E' else self.beliefs.human_position.area
            return (room != current_area and current_task.type != 'Caminar')
        
        else: return False
    

    def recompute(self):
        current_task = self.tasks[0]
        # returns tile where the object is or representative tile of area
        
        obj: Object = self.house.get_object(current_task.object_name)
        if obj is not None:
            if obj.carrier is None:
                dest_tile = obj.robot_face_tiles[0] if self.author == "Will-E" else obj.human_face_tiles[0]
            else: return False
        else: # then room is not None
            room = current_task.room
            dest_tile = self.house.get_room_tile(self.author, room)
            
        self.tasks.insert(0, Move(self.author, self.house, self.beliefs, dest_tile))
        return True
    
    def __repr__(self) -> str:
        finished = "finished"
        in_queue = "in queue"
        return f"{self.tasks.__repr__()} {finished if self.is_successful else in_queue}"
    
    def __str__(self) -> str:
        return f"({self.intention_name})"
    
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.is_successful = False

def generate_full_clean_living_room_plan(author: str, house: House, beliefs):
    tasks = []
    tasks.append(Move(author, house, beliefs, house.get_room_tile(author, 'sala_de_estar')))
    tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(480, 1200)), 'sala_de_estar'))
    for obj in livingroom_objects:
        living_obj: Object = house.get_object(obj)
        tasks.append(Move(author, house, beliefs, living_obj.robot_face_tiles[0]))
        tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(300, 600)), object=living_obj.name))
    return Plan("Realizar limpieza completa a la sala de estar", house, author, beliefs, tasks)


def generate_full_clean_bedroom_plan(author: str, house: House, beliefs):
    tasks = []
    tasks.append(Move(author, house, beliefs, house.get_room_tile(author, 'dormitorio')))
    tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(480, 1200)), 'dormitorio'))
    for obj in bedroom_objects:
        bed_obj: Object = house.get_object(obj)
        tasks.append(Move(author, house, beliefs, bed_obj.robot_face_tiles[0]))
        tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(300, 600)), object=bed_obj.name))
    return Plan("Realizar limpieza completa al dormitorio", house, author, beliefs, tasks)

def generate_full_clean_kitchen_plan(author: str, house: House, beliefs):
    tasks = []
    tasks.append(Move(author, house, beliefs, house.get_room_tile(author, 'cocina')))
    tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(480, 1200)), 'cocina'))
    for obj in kitchen_objects:
        kitchen_obj: Object = house.get_object(obj)
        tasks.append(Move(author, house, beliefs, kitchen_obj.robot_face_tiles[0]))
        tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(300, 600)), object=kitchen_obj.name))
    return Plan("Realizar limpieza completa a la cocina", house, author, beliefs, tasks)

def generate_clean_plan(author: str, house: House, beliefs):
    tasks = []
    for area in simulation_data.areas:
        tasks.append(Move(author, house, beliefs, house.get_room_tile(author, area)))
        tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(480, 1200)), area))
    return Plan("Limpiar la casa", house, author, beliefs, tasks)

def generate_water_plants_plan(author: str, house: House, beliefs):
    tasks = []
    for plant in plants:
        plant_obj: Object = house.get_object(plant)
        tasks.append(Move(author, house, beliefs, plant_obj.robot_face_tiles[0]))
        tasks.append(UseWater(author, house, beliefs, timedelta(seconds=15), object=plant_obj.name))
    return Plan("Regar las plantas", house, author, beliefs, tasks)

def generate_full_clean_bathroom_plan(author: str, house: House, beliefs):
    tasks = []
    tasks.append(Move(author, house, beliefs, house.get_room_tile(author, 'baño')))
    tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(480, 900)), 'baño'))
    for obj in bathroom_object:
        bath_obj: Object = house.get_object(obj)
        tasks.append(Move(author, house, beliefs, bath_obj.robot_face_tiles[0]))
        tasks.append(Clean(author, house, beliefs, timedelta(seconds=random.randint(300, 600)), object=bath_obj.name))
    return Plan("Realizar limpieza completa al baño", house, author, beliefs, tasks)

