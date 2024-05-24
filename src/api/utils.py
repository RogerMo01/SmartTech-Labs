
import random

def assert_chance(probability: float):
    chance = random.uniform(0,1)
    return chance <= probability