class Needs:
    def __init__(self):
        self.energy = 60
        self.hungry = 60
        self.bladder = 20
        self.hygiene = 60
        self.entertainment = 60

    def __getitem__(self, need: str):
        if need == 'energy':
            return self.energy
        elif need == 'hungry':
            return self.hungry
        elif need == 'bladder':
            return self.bladder
        elif need == 'hygiene':
            return self.hygiene
        elif need == 'entertainment':
            return self.entertainment
        else:
            raise Exception(f"No need named: {need}")
        
    def __setitem__(self, need: str, value):
        if value < 1 or value > 100:
            raise Exception(f"Value for {need} must be in range [1-100], but was: {value}")
        if need == 'energy':
            self.energy = value
        elif need == 'hungry':
            self.hungry = value
        elif need == 'bladder':
            self.bladder = value
        elif need == 'hygiene':
            self.hygiene = value
        elif need == 'entertainment':
            self.entertainment = value
        else:
            raise Exception(f"No need named: {need}")