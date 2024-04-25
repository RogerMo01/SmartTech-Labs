from Tile import Tile

class Task:
    def __init__(self, time):
        self.time = time         # timepo q toma en total
        self.elapsed_time = 0    # tiempo q se ha dedicado a la tarea
        self.postponed_time = 0  # timepo q lleva pospuesta

    def run(self):
        raise Exception(NotImplemented)
    

class Move(Task):
    def __init__(self, src: Tile, dest: Tile):
        self.elapsed_time = 0    # tiempo q se ha dedicado a la tarea
        self.src = src
        self.dest = dest

    def run(self):
        # llamar a la busqueda informada
        pass


# Other types of Tasks