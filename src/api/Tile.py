from Objects import Object

class Tile:
    """
    Represents a tile in the house map.

    Attributes:
        left (Tile): The tile to the left.
        up (Tile): The tile above.
        right (Tile): The tile to the right.
        down (Tile): The tile below.
        area (str): The area name were tile belongs.
        objects (set): Set of objects present on the tile.
    """
    def __init__(self, area, name, left=None, up=None, right=None, down=None):
        self.name = name
        self.left = left
        self.up = up
        self.right = right
        self.down = down

        self.area = area

        self.objects = set()

    def isTile(self) -> bool:
        return True
    def isWall(self) -> bool:
        return False
    def isBlank(self) -> bool:
        return False
    
    def add_object(self, obj: Object):
        self.objects.add(obj)

    def remove_object(self, obj: Object):
        self.objects.discard(obj)

    def contains(self, obj: Object):
        return obj in self.objects
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()        
    
class Wall(Tile):
    def __init__(self):
        pass
    def isWall(self) -> bool:
        return True
    def isTile(self) -> bool:
        return False
    
class Blank(Tile):
    def __init__(self):
        pass
    def isBlank(self) -> bool:
        return True
    def isTile(self) -> bool:
        return False
    
    