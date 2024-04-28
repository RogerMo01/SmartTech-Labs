import string
from Tile import Tile, Wall, Blank
from Objects import Object
from house_data import *

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class House:
    def __init__(self):
        
        # Dictionary matrix that allows O(1) access to tiles
        # [letter][number]
        self.map = map
        self.objects = {}

        House.build_house(self.map, self.objects)

        self.bot_position = self.map['J'][6]
        
        self.human_position = self.map['G'][9]

        # Contains conversations in the last step
        self.speaks = []

        # Contains conversations in current step
        self.speaks_stack = []

    
    def get_representative_tiles(self):
        rooms = []
        tiles = []
        for letter in self.map:
            for num in self.map[letter]:
                if not isinstance(self.map[letter][num], Blank) and not self.map[letter][num].area in rooms:
                    rooms.append(self.map[letter][num].area)
                    tiles.append(self.map[letter][num])
        return tiles
    
    def get_tile_by_room(self, room: str):
        representative_tiles = self.get_representative_tiles()
        return next((t for t in representative_tiles if t.area == room), None)
    

    def move(self, direction: str, author: str):
        if author == 'Bot':
            self.move_bot(direction)
        elif author == 'Human':
            self.move_human(direction)
        else:
            raise ValueError('Invalid author')
        
    def move_bot(self, direction: str):
        if direction == UP:
            self.bot_position = self.bot_position.up
        elif direction == DOWN:
            self.bot_position = self.bot_position.down
        elif direction == LEFT:
            self.bot_position = self.bot_position.left
        elif direction == RIGHT:
            self.bot_position = self.bot_position.right
        else:
            raise ValueError('Invalid direction')
        
    def move_human(self, direction: str):
        if direction == UP:
            self.human_position = self.human_position.up
        elif direction == DOWN:
            self.human_position = self.human_position.down
        elif direction == LEFT:
            self.human_position = self.human_position.left
        elif direction == RIGHT:
            self.human_position = self.human_position.right
        else:
            raise ValueError('Invalid direction')
        
    
    def say(self, speaker: str, sentence: str):
        '''Used for agents when they say something'''
        result = f"{speaker} dice: {sentence}"
        self.speaks_stack.append(result)

    def update_speaks(self):
        for i in self.speaks_stack:
            self.speaks.append(i)

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
        House.place_object(objects, sofa, [F7, F8], [E7, E8])
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
        

    @staticmethod
    def place_object(objects, obj: Object, tiles: list[Tile], face_tiles: list[Tile]):
        for t in tiles:
            t.add_object(obj)
        obj.face_tiles = face_tiles
        try:
            objects[obj] = face_tiles[0]
        except:
            raise Exception("face_tiles must have a first element")