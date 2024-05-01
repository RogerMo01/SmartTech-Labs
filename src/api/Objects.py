from abc import ABC

class Object(ABC):
    def __init__(self, name, portable=False, overlappable=False, human_step=False, robot_step=False, 
                 switchable=False, waterable=False, cleanable=False, sleppeable=False):
        self.name = name
        self.portable = portable
        self.overlappable = overlappable
        self.human_step = human_step
        self.robot_step = robot_step
        self.robot_face_tiles = []
        self.human_face_tiles = []
        self.switchable = switchable
        self.waterable = waterable
        self.cleanable = cleanable
        self.sleppeable = sleppeable

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    