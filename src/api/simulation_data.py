import string
from Tile import Tile, Wall, Blank
from Objects import Object

# A0 -> F5
A0 = Tile(area="dormitorio", name="A0")
A1 = Tile(area="dormitorio", name="A1")
A2 = Tile(area="dormitorio", name="A2")
A3 = Tile(area="dormitorio", name="A3")
A4 = Tile(area="dormitorio", name="A4")
A5 = Tile(area="dormitorio", name="A5")
B0 = Tile(area="dormitorio", name="B0")
B1 = Tile(area="dormitorio", name="B1")
B2 = Tile(area="dormitorio", name="B2")
B3 = Tile(area="dormitorio", name="B3")
B4 = Tile(area="dormitorio", name="B4")
B5 = Tile(area="dormitorio", name="B5")
C0 = Tile(area="dormitorio", name="C0")
C1 = Tile(area="dormitorio", name="C1")
C2 = Tile(area="dormitorio", name="C2")
C3 = Tile(area="dormitorio", name="C3")
C4 = Tile(area="dormitorio", name="C4")
C5 = Tile(area="dormitorio", name="C5")
D0 = Tile(area="dormitorio", name="D0")
D1 = Tile(area="dormitorio", name="D1")
D2 = Tile(area="dormitorio", name="D2")
D3 = Tile(area="dormitorio", name="D3")
D4 = Tile(area="dormitorio", name="D4")
D5 = Tile(area="dormitorio", name="D5")
E0 = Tile(area="dormitorio", name="E0")
E1 = Tile(area="dormitorio", name="E1")
E2 = Tile(area="dormitorio", name="E2")
E3 = Tile(area="dormitorio", name="E3")
E4 = Tile(area="dormitorio", name="E4")
E5 = Tile(area="dormitorio", name="E5")
F0 = Tile(area="dormitorio", name="F0")
F1 = Tile(area="dormitorio", name="F1")
F2 = Tile(area="dormitorio", name="F2")
F3 = Tile(area="dormitorio", name="F3")
F4 = Tile(area="dormitorio", name="F4")
F5 = Tile(area="dormitorio", name="F5")

# D6 -> F11
D6 = Tile(area="sala_de_estar", name="D6")
D7 = Tile(area="sala_de_estar", name="D7")
D8 = Tile(area="sala_de_estar", name="D8")
D9 = Tile(area="sala_de_estar", name="D9")
D10 = Tile(area="sala_de_estar", name="D10")
D11 = Tile(area="sala_de_estar", name="D11")
E6 = Tile(area="sala_de_estar", name="E6")
E7 = Tile(area="sala_de_estar", name="E7")
E8 = Tile(area="sala_de_estar", name="E8")
E9 = Tile(area="sala_de_estar", name="E9")
E10 = Tile(area="sala_de_estar", name="E10")
E11 = Tile(area="sala_de_estar", name="E11")
F6 = Tile(area="sala_de_estar", name="F6")
F7 = Tile(area="sala_de_estar", name="F7")
F8 = Tile(area="sala_de_estar", name="F8")
F9 = Tile(area="sala_de_estar", name="F9")
F10 = Tile(area="sala_de_estar", name="F10")
F11 = Tile(area="sala_de_estar", name="F11")
# G4 -> L11
G4 = Tile(area="sala_de_estar", name="G4")
G5 = Tile(area="sala_de_estar", name="G5")
G6 = Tile(area="sala_de_estar", name="G6")
G7 = Tile(area="sala_de_estar", name="G7")
G8 = Tile(area="sala_de_estar", name="G8")
G9 = Tile(area="sala_de_estar", name="G9")
G10 = Tile(area="sala_de_estar", name="G10")
G11 = Tile(area="sala_de_estar", name="G11")
H4 = Tile(area="sala_de_estar", name="H4")
H5 = Tile(area="sala_de_estar", name="H5")
H6 = Tile(area="sala_de_estar", name="H6")
H7 = Tile(area="sala_de_estar", name="H7")
H8 = Tile(area="sala_de_estar", name="H8")
H9 = Tile(area="sala_de_estar", name="H9")
H10 = Tile(area="sala_de_estar", name="H10")
H11 = Tile(area="sala_de_estar", name="H11")
I4 = Tile(area="sala_de_estar", name="I4")
I5 = Tile(area="sala_de_estar", name="I5")
I6 = Tile(area="sala_de_estar", name="I6")
I7 = Tile(area="sala_de_estar", name="I7")
I8 = Tile(area="sala_de_estar", name="I8")
I9 = Tile(area="sala_de_estar", name="I9")
I10 = Tile(area="sala_de_estar", name="I10")
I11 = Tile(area="sala_de_estar", name="I11")
J4 = Tile(area="sala_de_estar", name="J4")
J5 = Tile(area="sala_de_estar", name="J5")
J6 = Tile(area="sala_de_estar", name="J6")
J7 = Tile(area="sala_de_estar", name="J7")
J8 = Tile(area="sala_de_estar", name="J8")
J9 = Tile(area="sala_de_estar", name="J9")
J10 = Tile(area="sala_de_estar", name="J10")
J11 = Tile(area="sala_de_estar", name="J11")
K4 = Tile(area="sala_de_estar", name="K4")
K5 = Tile(area="sala_de_estar", name="K5")
K6 = Tile(area="sala_de_estar", name="K6")
K7 = Tile(area="sala_de_estar", name="K7")
K8 = Tile(area="sala_de_estar", name="K8")
K9 = Tile(area="sala_de_estar", name="K9")
K10 = Tile(area="sala_de_estar", name="K10")
K11 = Tile(area="sala_de_estar", name="K11")
L4 = Tile(area="sala_de_estar", name="L4")
L5 = Tile(area="sala_de_estar", name="L5")
L6 = Tile(area="sala_de_estar", name="L6")
L7 = Tile(area="sala_de_estar", name="L7")
L8 = Tile(area="sala_de_estar", name="L8")
L9 = Tile(area="sala_de_estar", name="L9")
L10 = Tile(area="sala_de_estar", name="L10")
L11 = Tile(area="sala_de_estar", name="L11")

# G0 -> I3
G0 = Tile(area="baño", name="G0")
G1 = Tile(area="baño", name="G1")
G2 = Tile(area="baño", name="G2")
G3 = Tile(area="baño", name="G3")
H0 = Tile(area="baño", name="H0")
H1 = Tile(area="baño", name="H1")
H2 = Tile(area="baño", name="H2")
H3 = Tile(area="baño", name="H3")
I0 = Tile(area="baño", name="I0")
I1 = Tile(area="baño", name="I1")
I2 = Tile(area="baño", name="I2")
I3 = Tile(area="baño", name="I3")

# J0 -> L3
J0 = Tile(area="cocina", name="J0")
J1 = Tile(area="cocina", name="J1")
J2 = Tile(area="cocina", name="J2")
J3 = Tile(area="cocina", name="J3")
K0 = Tile(area="cocina", name="K0")
K1 = Tile(area="cocina", name="K1")
K2 = Tile(area="cocina", name="K2")
K3 = Tile(area="cocina", name="K3")
L0 = Tile(area="cocina", name="L0")
L1 = Tile(area="cocina", name="L1")
L2 = Tile(area="cocina", name="L2")
L3 = Tile(area="cocina", name="L3")


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


map = {
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


################# Objects ##################
sofa = Object('sofá', human_step=True, cleanable=True)
table = Object('mesa_comedor', cleanable=True)
chair1 = Object('silla_1', overlappable=True, human_step=True, robot_step=True, cleanable=True)
chair2 = Object('silla_2', overlappable=True, human_step=True, robot_step=True, cleanable=True)
chair3 = Object('silla_3', overlappable=True, human_step=True, robot_step=True, cleanable=True)
chair4 = Object('silla_4', overlappable=True, human_step=True, robot_step=True, cleanable=True)
chair5 = Object('silla_5', overlappable=True, human_step=True, robot_step=True, cleanable=True)
chair6 = Object('silla_6', overlappable=True, human_step=True, robot_step=True, cleanable=True)
tv_table = Object('mesa_de_tv', overlappable=True, human_step=True, robot_step=True)
tv = Object('tv', overlappable=True, human_step=True, robot_step=True, switchable=True)

plant1 = Object('planta_1', overlappable=True, human_step=True, robot_step=True, waterable=True)
plant2 = Object('planta_2', overlappable=True, human_step=True, robot_step=True, waterable=True)
plant3 = Object('planta_3', overlappable=True, human_step=True, robot_step=True, waterable=True)

bed = Object('cama', human_step=True)
bed_table = Object('mesa_de_noche', overlappable=True, human_step=True, robot_step=True)
flip_flops = Object('chanclas', portable=True, overlappable=True, human_step=True, robot_step=True)
closet = Object('armario')
mobile = Object('móvil', portable=True, overlappable=True, human_step=True, robot_step=True)

toilet = Object('inodoro', overlappable=True, human_step=True, robot_step=True, cleanable=True)
bathtub = Object('bañera', cleanable=True)
washbasin = Object('lavamanos', overlappable=True, human_step=True, robot_step=True, cleanable=True)

worktop1 = Object('encimera_1', cleanable=True)
worktop2 = Object('encimera_2', cleanable=True)
worktop3 = Object('encimera_3', cleanable=True)
sink = Object('fregadero')
stove = Object('fogón')
bin = Object('cesto_de_basura', overlappable=True, human_step=True, robot_step=True)
fridge = Object('refrigerador')

objects_instances = [sofa, table, chair1, chair2, chair3, chair4, chair5, chair6, tv_table, tv,
                 plant1, plant2, plant3, bed, bed_table, flip_flops, closet, mobile,
                 toilet, bathtub, washbasin, worktop1, worktop2, worktop3, sink, stove, bin, fridge]
objects_names = [o.name for o in objects_instances]


#################### Areas #####################
areas = ['dormitorio', 'sala_de_estar', 'baño', 'cocina']


#################### Robot Actions ########################
CLEAN = "LIMPIAR"
WALK = "CAMINAR_HASTA"
# NOTIFY = "AVISAR"

WATER_OBJ = "ECHAR_AGUA_A"
ON_OBJ = "ENCENDER"
OFF_OBJ = "APAGAR"
TAKE_OBJ = "COGER"
DROP_OBJ = "SOLTAR"
SET_UP = "PREPARAR"

PLAY_MUSIC = "REPRODUCIR_MÚSICA"

SAY_JOKE = "DECIR_CHISTE"

RECOMMEND = "HACER_RECOMENDACIÓN"

robot_need_actions = [PLAY_MUSIC] 
robot_actions = actions = [WALK, CLEAN, WATER_OBJ, ON_OBJ, OFF_OBJ, TAKE_OBJ, DROP_OBJ, PLAY_MUSIC, SET_UP]
robot_obj_actions = actions = [WALK, CLEAN, WATER_OBJ, ON_OBJ, OFF_OBJ, TAKE_OBJ, DROP_OBJ, SET_UP]
robot_no_obj_actions = [PLAY_MUSIC]
robot_area_actions = [WALK, CLEAN]

robot_water_actions = [CLEAN, WATER_OBJ]


ENERGY = 'energy'
BLADDER = 'bladder'
HUNGRY = 'hungry'
HYGIENE = 'hygiene'
ENTERTAINMENT = 'entertainment'
 
NEEDS_LIMIT = {'bladder': 20, 'hungry': 30, 'energy': 15, 'hygiene': 10, 'entertainment': 10}
BEST_TIMES = {'bladder': 900, 'hungry': 1800, 'energy': 28800, 'hygiene': 1200, 'entertainment': 9000}
# siente la necesidad cada estos numeros (ejemplo: sueño cada 16 horas)
# energy: 16*3600, hygiene: 31*3600, 4*3600[miccionar]
DEC_LIMIT = {'bladder': 14400, 'hungry': 50400, 'energy': 57600, 'hygiene': 111600, 'entertainment': 64800}