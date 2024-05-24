from simulation_data import DEC_LIMIT, NEEDS_LIMIT, ENERGY, HYGIENE, HUNGRY, BLADDER, ENTERTAINMENT

class Needs:
    def __init__(self):
        self.energy = 99
        self.hungry = 30
        self.bladder = 20
        self.hygiene = 70
        self.entertainment = 50

    def __getitem__(self, need: str):
        if need == ENERGY:
            return self.energy
        elif need == HUNGRY:
            return self.hungry
        elif need == BLADDER:
            return self.bladder
        elif need == HYGIENE:
            return self.hygiene
        elif need == ENTERTAINMENT:
            return self.entertainment
        else:
            raise Exception(f"No need named: {need}")
        
    def __setitem__(self, need: str, value):
        if value < 1 or value > 100:
            raise Exception(f"Value for {need} must be in range [1-100], but was: {value}")
        if need == ENERGY:
            self.energy = value
        elif need == HUNGRY:
            self.hungry = value
        elif need == BLADDER:
            self.bladder = value
        elif need == HYGIENE:
            self.hygiene = value
        elif need == ENTERTAINMENT:
            self.entertainment = value
        else:
            raise Exception(f"No need named: {need}")
        
    def sum_level(self, need, level):
        sum = self[need] + level
        if sum > 100:
            self[need] = 100
        else: self[need]=sum

    def dec_level(self, need):
        result = self[need] - (100-NEEDS_LIMIT[need])/DEC_LIMIT[need]
        if result < 1:
            self[need] = 1
        else:
            self[need] = result
    
    def __str__(self) -> str:
        return f"""
{HUNGRY}        : {self.hungry}
{BLADDER}       : {self.bladder}
{HYGIENE}       : {self.hygiene}
{ENTERTAINMENT} : {self.entertainment}
{ENERGY}        : {self.energy}
        """
    
    def __repr__(self) -> str:
        return self.__str__()