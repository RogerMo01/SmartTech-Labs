import string
from Tile import Tile, Wall, Blank
from Objects import Object
from simulation_data import *
import random
# from agents.bdi_agent import BDI_Agent

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class House:
    def __init__(self):
        
        # Dictionary matrix that allows O(1) access to tiles
        # [letter][number]
        self.__map = map
        self.__objects = {}

        House.build_house(self.__map, self.__objects)

        self.__bot_position = self.__map['D'][3]
        
        self.__human_position = self.__map['G'][9]

        # Contains conversations in the last second
        self.__speaks = []

        # Contains conversations in current second
        self.__speaks_stack = []

        self.__is_music_playing = False



    def get_is_music_playing(self): return self.__is_music_playing

    def set_is_music_playing(self, value: bool):
        self.__is_music_playing = value

    
    def get_representative_tiles(self):
        rooms = []
        tiles = []
        for letter in self.__map:
            for num in self.__map[letter]:
                if not isinstance(self.__map[letter][num], Blank) and not self.__map[letter][num].area in rooms:
                    rooms.append(self.__map[letter][num].area)
                    tiles.append(self.__map[letter][num])
        return tiles
    
    def get_tile_by_room(self, room: str):
        representative_tiles: list[Tile] = self.get_representative_tiles()
        return next((t for t in representative_tiles if t.area == room), None)
    

    def get_room_tile(self, agent: str, room: str):
        """Returns a random tile located in an specific room where agent can step"""
        tiles = self._get_all_rooms_tiles()
        tiles: list[Tile] = tiles[room]
        tiles = [x for x in tiles if self._can_walk_tile(x, agent)]
        return random.choice(tiles)
    
    def _can_walk_tile(self, tile: Tile, agent: str):
        """Returns if the agent can step on this tile"""
        for o in tile.objects:
            if agent == 'Will-E' and not o.robot_step:
                return False
            if agent == 'Pedro' and not o.human_step:
                return False
        return True

    def _get_all_rooms_tiles(self):
        """Returns a dictionary of all tiles for each area"""
        tiles = dict()
        for letter in self.__map:
            for num in self.__map[letter]:
                tile: Tile = self.__map[letter][num]
                if tile.isTile():
                    try:
                        tiles[tile.area].append(tile)
                    except:
                        tiles[tile.area] = [tile]
        return tiles

    
    def get_data(self):
        return self.__map.copy(), self.__objects.copy(), self.__bot_position, self.__human_position, self.__speaks.copy()

    def get_object(self, name):
        for o in list(self.__objects.keys()):
            if o.name == name:
                return o
        return None
    

    def take_object(self, agent, obj: Object):
        """For agents to take and carry specific object"""
        tiles: list[Tile] = self.__objects[obj]  # tiles occupied by obj
        for t in tiles: t.objects.remove(obj)    # remove object from tiles
        self.__objects[obj] = agent              # set object location as Agent
        obj.robot_face_tiles = None                    # clear face tiles
        obj.human_face_tiles = None 
        obj.carrier = agent 
        

    def drop_object(self, agent, obj: Object):
        """For agents to drop specific object"""
        tiles: list[Tile] = [self.__bot_position]  # BOOM if object takes multiple tiles
        for t in tiles: t.objects.add(obj)
        self.__objects[obj] = tiles
        obj.robot_face_tiles = tiles
        obj.human_face_tiles = tiles
        obj.carrier = None  

    def move(self, direction: str, author: str):
        if author == 'Will-E':
            self.move_bot(direction)
        elif author == 'Pedro':
            self.move_human(direction)
        else:
            raise ValueError('Invalid author')
        return self.__bot_position
        
        
    def move_bot(self, direction: str):
        if direction == UP:
            self.__bot_position = self.__bot_position.up
        elif direction == DOWN:
            self.__bot_position = self.__bot_position.down
        elif direction == LEFT:
            self.__bot_position = self.__bot_position.left
        elif direction == RIGHT:
            self.__bot_position = self.__bot_position.right
        else:
            raise ValueError('Invalid direction')

        
    def move_human(self, direction: str):
        if direction == UP:
            self.__human_position = self.__human_position.up
        elif direction == DOWN:
            self.__human_position = self.__human_position.down
        elif direction == LEFT:
            self.__human_position = self.__human_position.left
        elif direction == RIGHT:
            self.__human_position = self.__human_position.right
        else:
            raise ValueError('Invalid direction')
        
    
    def say(self, speaker: str, sentence: str, by_human_for_need:bool = False):
        '''Used for agents when they say something'''
        result = f"{speaker} dice: {sentence}"
        self.__speaks_stack.append((result, by_human_for_need))

    def update_speaks(self):
        self.__speaks = []
        for i in self.__speaks_stack:
            self.__speaks.append(i)
        self.__speaks_stack = []

    @staticmethod
    def build_house(map, objects):

        letters = list(string.ascii_uppercase)

        # Set neightbors
        for i in range(12):
            letter = letters[i]
            for j in range(12):
                num = j

                tile: Tile = map[letter][num]

                if i > 0:
                    up: Tile = map[letters[i-1]][num]
                    tile.up = up
                    up.down = tile

                if i < 11:
                    down: Tile = map[letters[i+1]][num]
                    tile.down = down
                    down.up = tile

                if j > 0:
                    left: Tile = map[letter][num-1]
                    tile.left = left
                    left.right = tile

                if j < 11:
                    right: Tile = map[letter][num+1]
                    tile.right = right
                    right.left = tile

        # Set walls
        for i in range(12):
            letter = letters[i]
            for j in range(12):
                num = j
                tile: Tile = map[letter][num]

                wall = Wall()

                # wall up
                if (letter == 'A' and j < 6) or (letter == 'D' and j > 5) or (letter == 'G' and j < 5) or (letter == 'J' and j < 4):
                    tile.up = wall

                # wall down
                if (letter == 'F' and j < 5) or (letter == 'I' and j < 4) or (letter == 'L'):
                    tile.down = wall
                
                # wall on left
                if (j == 0) or (letter in ['H', 'I'] and j == 4) or (letter in ['D', 'E', 'F'] and j == 6):
                    tile.left = wall
                
                # wall on right
                if (letter in ['H', 'I'] and j == 3) or (letter in ['A', 'B', 'C', 'D', 'E', 'F'] and j == 5) or (letter in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'] and j == 11):
                    tile.right = wall

        # Set objects
        House.place_object(objects, sofa, [F7, F8], [E7, E8], [F7, F8])
        House.place_object(objects, table, [I7, I8], [H7, H8, I9, J8, J7, I6])
        House.place_object(objects, chair1, [H7], [H7])
        House.place_object(objects, chair2, [H8], [H8])
        House.place_object(objects, chair3, [I9], [I9])
        House.place_object(objects, chair4, [J8], [J8])
        House.place_object(objects, chair5, [J7], [J7])
        House.place_object(objects, chair6, [I6], [I6])
        House.place_object(objects, plant1, [D6], [D6])
        House.place_object(objects, plant2, [J0], [J0])
        House.place_object(objects, plant3, [A5], [A5])
        House.place_object(objects, tv_table, [D7, D8], [D7, D8])
        House.place_object(objects, tv, [D7, D8], [D7, D8])
        House.place_object(objects, coffee_dispenser, [D11], [D11])
        House.place_object(objects, bed, [C0, C1, D0, D1], [B1, E1], [C0, C1, D0, D1])
        House.place_object(objects, bed_table, [B0], [B0])
        House.place_object(objects, flip_flops, [B1], [B1])
        House.place_object(objects, closet, [B5, C5], [B4, C4])
        House.place_object(objects, mobile, [B0], [B0])
        House.place_object(objects, toilet, [I2], [I2])
        House.place_object(objects, bathtub, [G0, H0], [H1], [G0, H0])
        House.place_object(objects, washbasin, [G2], [G2])
        House.place_object(objects, worktop1, [L0], [K1])
        House.place_object(objects, worktop2, [L1], [K1])
        House.place_object(objects, worktop3, [L3], [K3])
        House.place_object(objects, sink, [L2], [K2])
        House.place_object(objects, stove, [K0], [K1])
        House.place_object(objects, bin, [L4], [L4])
        House.place_object(objects, fridge, [J2], [K2])
        

        

    @staticmethod
    def place_object(objects, obj: Object, tiles: list[Tile], robot_face_tiles: list[Tile], human_face_tiles: list[Tile] = None):
        for t in tiles:
            t.add_object(obj)
        obj.robot_face_tiles = robot_face_tiles
        if human_face_tiles:
            obj.human_face_tiles = human_face_tiles
        else:
            obj.human_face_tiles = robot_face_tiles
            
        try:
            objects[obj] = tiles
        except:
            raise Exception("face_tiles must have a first element")