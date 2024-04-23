import string
from Tile import Tile, Wall, Blank
from Objects import Object

# A0 -> F5
A0 = Tile(area="bedroom", name="A0")
A1 = Tile(area="bedroom", name="A1")
A2 = Tile(area="bedroom", name="A2")
A3 = Tile(area="bedroom", name="A3")
A4 = Tile(area="bedroom", name="A4")
A5 = Tile(area="bedroom", name="A5")
B0 = Tile(area="bedroom", name="B0")
B1 = Tile(area="bedroom", name="B1")
B2 = Tile(area="bedroom", name="B2")
B3 = Tile(area="bedroom", name="B3")
B4 = Tile(area="bedroom", name="B4")
B5 = Tile(area="bedroom", name="B5")
C0 = Tile(area="bedroom", name="C0")
C1 = Tile(area="bedroom", name="C1")
C2 = Tile(area="bedroom", name="C2")
C3 = Tile(area="bedroom", name="C3")
C4 = Tile(area="bedroom", name="C4")
C5 = Tile(area="bedroom", name="C5")
D0 = Tile(area="bedroom", name="D0")
D1 = Tile(area="bedroom", name="D1")
D2 = Tile(area="bedroom", name="D2")
D3 = Tile(area="bedroom", name="D3")
D4 = Tile(area="bedroom", name="D4")
D5 = Tile(area="bedroom", name="D5")
E0 = Tile(area="bedroom", name="E0")
E1 = Tile(area="bedroom", name="E1")
E2 = Tile(area="bedroom", name="E2")
E3 = Tile(area="bedroom", name="E3")
E4 = Tile(area="bedroom", name="E4")
E5 = Tile(area="bedroom", name="E5")
F0 = Tile(area="bedroom", name="F0")
F1 = Tile(area="bedroom", name="F1")
F2 = Tile(area="bedroom", name="F2")
F3 = Tile(area="bedroom", name="F3")
F4 = Tile(area="bedroom", name="F4")
F5 = Tile(area="bedroom", name="F5")

# D6 -> F11
D6 = Tile(area="livingroom", name="D6")
D7 = Tile(area="livingroom", name="D7")
D8 = Tile(area="livingroom", name="D8")
D9 = Tile(area="livingroom", name="D9")
D10 = Tile(area="livingroom", name="D10")
D11 = Tile(area="livingroom", name="D11")
E6 = Tile(area="livingroom", name="E6")
E7 = Tile(area="livingroom", name="E7")
E8 = Tile(area="livingroom", name="E8")
E9 = Tile(area="livingroom", name="E9")
E10 = Tile(area="livingroom", name="E10")
E11 = Tile(area="livingroom", name="E11")
F6 = Tile(area="livingroom", name="F6")
F7 = Tile(area="livingroom", name="F7")
F8 = Tile(area="livingroom", name="F8")
F9 = Tile(area="livingroom", name="F9")
F10 = Tile(area="livingroom", name="F10")
F11 = Tile(area="livingroom", name="F11")
# G4 -> L11
G4 = Tile(area="livingroom", name="G4")
G5 = Tile(area="livingroom", name="G5")
G6 = Tile(area="livingroom", name="G6")
G7 = Tile(area="livingroom", name="G7")
G8 = Tile(area="livingroom", name="G8")
G9 = Tile(area="livingroom", name="G9")
G10 = Tile(area="livingroom", name="G10")
G11 = Tile(area="livingroom", name="G11")
H4 = Tile(area="livingroom", name="H4")
H5 = Tile(area="livingroom", name="H5")
H6 = Tile(area="livingroom", name="H6")
H7 = Tile(area="livingroom", name="H7")
H8 = Tile(area="livingroom", name="H8")
H9 = Tile(area="livingroom", name="H9")
H10 = Tile(area="livingroom", name="H10")
H11 = Tile(area="livingroom", name="H11")
I4 = Tile(area="livingroom", name="I4")
I5 = Tile(area="livingroom", name="I5")
I6 = Tile(area="livingroom", name="I6")
I7 = Tile(area="livingroom", name="I7")
I8 = Tile(area="livingroom", name="I8")
I9 = Tile(area="livingroom", name="I9")
I10 = Tile(area="livingroom", name="I10")
I11 = Tile(area="livingroom", name="I11")
J4 = Tile(area="livingroom", name="J4")
J5 = Tile(area="livingroom", name="J5")
J6 = Tile(area="livingroom", name="J6")
J7 = Tile(area="livingroom", name="J7")
J8 = Tile(area="livingroom", name="J8")
J9 = Tile(area="livingroom", name="J9")
J10 = Tile(area="livingroom", name="J10")
J11 = Tile(area="livingroom", name="J11")
K4 = Tile(area="livingroom", name="K4")
K5 = Tile(area="livingroom", name="K5")
K6 = Tile(area="livingroom", name="K6")
K7 = Tile(area="livingroom", name="K7")
K8 = Tile(area="livingroom", name="K8")
K9 = Tile(area="livingroom", name="K9")
K10 = Tile(area="livingroom", name="K10")
K11 = Tile(area="livingroom", name="K11")
L4 = Tile(area="livingroom", name="L4")
L5 = Tile(area="livingroom", name="L5")
L6 = Tile(area="livingroom", name="L6")
L7 = Tile(area="livingroom", name="L7")
L8 = Tile(area="livingroom", name="L8")
L9 = Tile(area="livingroom", name="L9")
L10 = Tile(area="livingroom", name="L10")
L11 = Tile(area="livingroom", name="L11")

# G0 -> I3
G0 = Tile(area="bathroom", name="G0")
G1 = Tile(area="bathroom", name="G1")
G2 = Tile(area="bathroom", name="G2")
G3 = Tile(area="bathroom", name="G3")
H0 = Tile(area="bathroom", name="H0")
H1 = Tile(area="bathroom", name="H1")
H2 = Tile(area="bathroom", name="H2")
H3 = Tile(area="bathroom", name="H3")
I0 = Tile(area="bathroom", name="I0")
I1 = Tile(area="bathroom", name="I1")
I2 = Tile(area="bathroom", name="I2")
I3 = Tile(area="bathroom", name="I3")

# J0 -> L3
J0 = Tile(area="bathroom", name="J0")
J1 = Tile(area="bathroom", name="J1")
J2 = Tile(area="bathroom", name="J2")
J3 = Tile(area="bathroom", name="J3")
K0 = Tile(area="bathroom", name="K0")
K1 = Tile(area="bathroom", name="K1")
K2 = Tile(area="bathroom", name="K2")
K3 = Tile(area="bathroom", name="K3")
L0 = Tile(area="bathroom", name="L0")
L1 = Tile(area="bathroom", name="L1")
L2 = Tile(area="bathroom", name="L2")
L3 = Tile(area="bathroom", name="L3")


# A6 -> C11
A6 = Blank()
A7 = Blank()
A8 = Blank()
A9 = Blank()
A10 = Blank()
A11 = Blank()
B6 = Blank()
B7 = Blank()
B8 = Blank()
B9 = Blank()
B10 = Blank()
B11 = Blank()
C6 = Blank()
C7 = Blank()
C8 = Blank()
C9 = Blank()
C10 = Blank()
C11 = Blank()

# Objects instance
sofa = Object('Sofa', human_step=True)
table = Object('Table')
chair1 = Object('Chair #1', overlappable=True, human_step=True, robot_step=True)
chair2 = Object('Chair #2', overlappable=True, human_step=True, robot_step=True)
chair3 = Object('Chair #3', overlappable=True, human_step=True, robot_step=True)
chair4 = Object('Chair #4', overlappable=True, human_step=True, robot_step=True)
chair5 = Object('Chair #5', overlappable=True, human_step=True, robot_step=True)
chair6 = Object('Chair #6', overlappable=True, human_step=True, robot_step=True)
plant1 = Object('Plant #1', overlappable=True, human_step=True, robot_step=True)
plant2 = Object('Plant #2', overlappable=True, human_step=True, robot_step=True)
plant3 = Object('Plant #3', overlappable=True, human_step=True, robot_step=True)
tv_table = Object('Tv Table', overlappable=True, human_step=True, robot_step=True)


class House:
    def __init__(self):

        # Dictionary matrix that allows O(1) access to tiles
        # [letter][number]
        self.map = {
            'A': {0: A0, 1: A1, 2: A2, 3: A3, 4: A4, 5: A5, 6: A6, 7: A7, 8: A8, 9: A9, 10: A10, 11: A11},
            'B': {0: B0, 1: B1, 2: B2, 3: B3, 4: B4, 5: B5, 6: B6, 7: B7, 8: B8, 9: B9, 10: B10, 11: B11},
            'C': {0: C0, 1: C1, 2: C2, 3: C3, 4: C4, 5: C5, 6: C6, 7: C7, 8: C8, 9: C9, 10: C10, 11: C11},
            'D': {0: D0, 1: D1, 2: D2, 3: D3, 4: D4, 5: D5, 6: D6, 7: D7, 8: D8, 9: D9, 10: D10, 11: D11},
            'E': {0: E0, 1: E1, 2: E2, 3: E3, 4: E4, 5: E5, 6: E6, 7: E7, 8: E8, 9: E9, 10: E10, 11: E11},
            'F': {0: F0, 1: F1, 2: F2, 3: F3, 4: F4, 5: F5, 6: F6, 7: F7, 8: F8, 9: F9, 10: F10, 11: F11},
            'G': {0: G0, 1: G1, 2: G2, 3: G3, 4: G4, 5: G5, 6: G6, 7: G7, 8: G8, 9: G9, 10: G10, 11: G11},
            'H': {0: H0, 1: H1, 2: H2, 3: H3, 4: H4, 5: H5, 6: H6, 7: H7, 8: H8, 9: H9, 10: H10, 11: H11},
            'I': {0: I0, 1: I1, 2: I2, 3: I3, 4: I4, 5: I5, 6: I6, 7: I7, 8: I8, 9: I9, 10: I10, 11: I11},
            'J': {0: J0, 1: J1, 2: J2, 3: J3, 4: J4, 5: J5, 6: J6, 7: J7, 8: J8, 9: J9, 10: J10, 11: J11},
            'K': {0: K0, 1: K1, 2: K2, 3: K3, 4: K4, 5: K5, 6: K6, 7: K7, 8: K8, 9: K9, 10: K10, 11: K11},
            'L': {0: L0, 1: L1, 2: L2, 3: L3, 4: L4, 5: L5, 6: L6, 7: L7, 8: L8, 9: L9, 10: L10, 11: L11}
        }
        self.objects = {}

        self.build_house()

        self.bot_position = self.map['A'][0]

    def build_house(self):

        letters = list(string.ascii_uppercase)

        # Set neightbors
        for i in range(12):
            letter = letters[i]
            for j in range(12):
                num = j

                tile: Tile = self.map[letter][num]

                if i > 0:
                    up: Tile = self.map[letters[i-1]][num]
                    tile.up = up
                    up.down = tile

                if i < 11:
                    down: Tile = self.map[letters[i+1]][num]
                    tile.down = down
                    down.up = tile

                if j > 0:
                    left: Tile = self.map[letter][num-1]
                    tile.left = left
                    left.right = tile

                if j < 11:
                    right: Tile = self.map[letter][num+1]
                    tile.right = right
                    right.left = tile

        # Set walls
        for i in range(12):
            letter = letters[i]
            for j in range(12):
                num = j
                tile: Tile = self.map[letter][num]

                wall = Wall()

                # wall up
                if (letter == 'A' and j < 6) or (letter == 'D' and j > 5) or (letter == 'G' and j < 5) or (letter == 'J' and j < 4):
                    tile.up = wall

                # wall down
                if (letter == 'F' and j < 5) and (letter == 'I' and j < 4) and (letter == 'L'):
                    tile.down = wall
                
                # wall on left
                if (j == 0) and (letter in ['H', 'I'] and j == 4) and (letter in ['D', 'E', 'F'] and j == 6):
                    tile.left = wall
                
                # wall on right
                if (letter in ['H', 'I'] and j == 3) or (letter in ['A', 'B', 'C', 'D', 'E', 'F'] and j == 5) or (letter in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']):
                    tile.right = wall

        # Set objects
        self.place_object(sofa, [F7, F8], [E7, E8])
        self.place_object(table, [I7, I8], [H7, H8, I9, J8, J7, I6])
        self.place_object(chair1, [H7], [H7])
        self.place_object(chair2, [H8], [H8])
        self.place_object(chair3, [I9], [I9])
        self.place_object(chair4, [J8], [J8])
        self.place_object(chair5, [J7], [J7])
        self.place_object(chair6, [I6], [I6])
        self.place_object(plant1, [D6], [D6])
        self.place_object(plant2, [J0], [J0])
        self.place_object(plant3, [A5], [A5])
        self.place_object(tv_table, [D7, D8], [D7, D8])
        


    def place_object(self, obj: Object, tiles: list[Tile], face_tiles: list[Tile]):
        for t in tiles:
            t.add_object(sofa)
        sofa.face_tiles = face_tiles
        try:
            self.objects[obj] = face_tiles[0]
        except:
            raise Exception("face_tiles must have a first element")