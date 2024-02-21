import random
from math import sqrt
import time
import math
import copy

# Function to generate a random grid with shuffled elements
def generate_random_grid():
    chars = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'B']
    random.shuffle(chars)
    r_grid = [chars[i:i+3] for i in range(0, 9, 3)]
    return r_grid

# Breadth-First Search algorithm to find a path from a given grid to the target grid
def normal(top, target, blank=False):
    return 0

def tilesDisplaced(top, target, blank=False):
    tiles_displaced = 0

    for i in range(3):
        for j in range(3):
            if top[i][j] == 'B' and not blank:
                continue
            if top[i][j] != target[i][j]:
                tiles_displaced += 1

    return tiles_displaced

def manhattanDist(top, target, blank=False):
    manhattan_distance = 0
    map = {}
    for i in range(3):
        for j in range(3):
            map[top[i][j]] = (i, j)

    for i in range(3):
        for j in range(3):
            x, y = map[target[i][j]]
            if target[i][j] == 'B' and not blank:
                continue
            manhattan_distance += abs(x - i) + abs(y - j)

    return manhattan_distance

def euclid(top, target, blank=False):
    distance = 0
    map = {}
    for i in range(3):
        for j in range(3):
            map[top[i][j]] = (i, j)

    for i in range(3):
        for j in range(3):
            x, y = map[target[i][j]]
            if target[i][j] == 'B' and not blank:
                continue
            distance += sqrt((x - i) ** 2 + (y - j) ** 2)

    return distance

def heuristic(grid, target, k):
    if k == 1:
        return normal(grid, target)
    if k == 2:
        return tilesDisplaced(grid, target)
    if k == 3:
        return manhattanDist(grid, target)
    if k == 4:
        return euclid(grid, target)

# Decreasing temperature linearly with time
def temperature(time):
    return 10000- time

# Get probability of choosing a bad state/ backward step
def probability(temperature, difference):
    if difference > 0:
        # New state has a lower value
        return 1

    return (math.e**((difference) / temperature))

lst = ["", "normal", "tilesdisplaced", "manhatt_distance", "euclid_distance"]

def simulated_annealing(grid1, target, max_iterations, k):
    visited = set()
    #parent = {tuple(map(tuple, grid)): ((), -1)}
    state_list = []
    grid=copy.deepcopy(grid1)
    state_list.append(tuple(copy.deepcopy(grid)))
    for _ in range(max_iterations):
        top_tuples = [tuple(row) for row in grid]

        if grid == target:
            total_states_explored = len(visited)
            return state_list, total_states_explored

        visited.add(tuple(top_tuples))
        current_temperature = temperature(_)

        x, y = None, None
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 'B':
                    x, y = i, j
                    break

        if x is not None and y is not None:
            # Choose one random move among the possible moves
            moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random_direction = random.choice(moves)
            new_x, new_y = x + random_direction[0], y + random_direction[1]

            if 0 <= new_x < 3 and 0 <= new_y < 3:
                index1 = (x, y)
                index2 = (new_x, new_y)
                top_tuples = [tuple(row) for row in grid]
                current_value = heuristic(top_tuples, target, k)
                # Calculate the neighbor's value and its tuple representation
                grid[index1[0]][index1[1]], grid[index2[0]][index2[1]] = grid[index2[0]][index2[1]], grid[index1[0]][index1[1]]
                top_tuples = [tuple(row) for row in grid]
                neighbor_value = heuristic(top_tuples, target, k)

                # Calculate the difference in values
                difference = current_value-neighbor_value


                if  difference >0 or random.random() < probability(current_temperature, difference):
                     state_list.append(tuple(copy.deepcopy(grid)))
                else:
                    grid[index1[0]][index1[1]], grid[index2[0]][index2[1]] = grid[index2[0]][index2[1]], grid[index1[0]][index1[1]]  # Revert the swap if the move is not accepted
                    state_list.append(tuple(copy.deepcopy(grid)))

    print(f"Total states visited = {len(visited)}")
    return False



def print_path(state_list):
    print("--------------\nOptimal Path: ")
    cnt = 0
    if len(state_list) > 100:
        print("Number of states exceeded 100. Printing the first 100 states:")
        state_list = state_list[:100]
    for state in state_list:
        print(f"Move {cnt}:")
        print(state)
        cnt += 1


def swap(arr, index1, index2):
    arr[index1[0]][index1[1]], arr[index2[0]][index2[1]] = arr[index2[0]][index2[1]], arr[index1[0]][index1[1]]

current_state=[['T1', 'T2', 'T3'], ['T4', 'B', 'T6'], ['T7', 'T5', 'T8']]
#current_state=generate_random_grid()
target = [['T1', 'T2', 'T3'], ['T4', 'T5', 'T6'], ['T7', 'T8', 'B']]

print("Source:")
for row in current_state:
    print(row)

print("Target:")
for row in target:
    print(row)

tp = [tuple(row) for row in current_state]

for k in range(2, 4):
    print("--------------\n")
    start = time.time()
    visited = set()
    grid1=current_state
    print("Source:")
    for row in grid1:
       print(row)
    result = simulated_annealing(grid1, target, 10000, k)
    end = time.time()

    if result:
        path_list, total_states_explored = result
        print(f"Target state reached using {lst[k]}")
        print_path(path_list)
        print(f"Total states explored: {total_states_explored}")
        print(f"Total number of states in the optimal path or cost : {len(path_list) -1}")
    else:
        print(f"Target state not reached using {lst[k]}")
#
    print("Time taken for execution:", end - start)
