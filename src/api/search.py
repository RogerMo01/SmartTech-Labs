import heapq
import math
from collections import deque
from Tile import Tile
from House import *


class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When you create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 
        
    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)
    

class Node:
    "A Node in a search tree."
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost
    
    
failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.
    
    
def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)
        

def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state]


FIFOQueue = deque

LIFOQueue = list

class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]
    
    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)


def best_first_search(problem, f):
    "Search nodes with minimum f(node) value first."
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return failure


def g(n): return n.path_cost


def astar_search(problem, h=None):
    """Search nodes with minimum f(n) = g(n) + h(n)."""
    h = h or problem.h
    return best_first_search(problem, f=lambda n: g(n) + h(n))






UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

BOT = 'bot'
HUMAN = 'human'

class WalkProblem(Problem):
    def __init__(self, initial: Tile, goal: Tile, agent='bot'):
        self.initial = initial
        self.goal = goal
        self.agent = agent
        self.manhattan = compute_manhattan(goal.name)
        

    def actions(self, state: Tile):
        response = []
        if self.is_valid_tile(state.up):
            response.append(UP)
        if self.is_valid_tile(state.down):
            response.append(DOWN)
        if self.is_valid_tile(state.left):
            response.append(LEFT)
        if self.is_valid_tile(state.right):
            response.append(RIGHT)
        
        return tuple(response)
    
    
    def is_valid_tile(self, next: Tile):

        continue_cut = (next is not None) and next.isTile()
        if not continue_cut:
            return False
        else:
            for obj in list(next.objects):
                if (self.agent == BOT and not obj.robot_step) or (self.agent == HUMAN and not obj.human_step):
                    return False
        return True

    
    def result(self, state: Tile, action):
        if action == UP:
            return state.up
        if action == DOWN:
            return state.down
        if action == LEFT:
            return state.left
        if action == RIGHT:
            return state.right
    
    # Manhattan distance
    def h(self, node):
        state = node.state
        letter = state.name[0]
        num = int(state.name[1])
        return self.manhattan[letter][num]
    
    def solve(self):
        sln = astar_search(self)
        actions = path_actions(sln)
        return actions

    
def compute_manhattan(goal: str, size=12):
    response = {}

    g_letter, g_num = goal[0], int(goal[1])

    # Get letters list
    letters = list(string.ascii_uppercase)[0:size]

    for l in letters:
        response[l] = {}

    g_index = letters.index(g_letter)
    
    for i, letter in enumerate(letters):
        for j in range(12):
            response[letter][j] = abs(i-g_index) + abs(j-int(g_num))
    
    return response
