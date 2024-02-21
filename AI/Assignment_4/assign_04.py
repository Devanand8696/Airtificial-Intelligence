import random
from math import sqrt
import time

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

lst = ["", "normal", "tilesdisplaced", "manhatt_distance", "euclid_distance"]

def hillClimber(grid, target, k, visited, parent):
    top_tuples = [tuple(row) for row in grid]
    if tuple(top_tuples) in visited:
        print(f"Total states visited = {len(visited)}")
        return False
    top_tuples_target = [tuple(row) for row in target]

    # Printing the path if the goal is reached
    if grid == target:
        state = tuple(top_tuples)
        state_list = []
        while state in parent:
            state_list.append(state)
            state = parent[state][0]
        state_list.reverse()  # Reverse the list to print from initial state to goal state

        # Count the total number of states explored
        total_states_explored = len(visited)

        return state_list, total_states_explored

    visited.add(tuple(top_tuples))

    # Traversing over the neighbors and selecting the most optimal neighbor
    # that is better than the current node
    mnh = heuristic(grid, target, k)

    nxtgrid = top_tuples
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for i in range(3):
        for j in range(3):
            if grid[i][j] == 'B':
                x, y = i, j
                for dx, dy in moves:
                    if 0 <= x + dx < 3 and 0 <= y + dy < 3:
                        index1 = (x, y)
                        index2 = (x + dx, y + dy)
                        swap(grid, index1, index2)
                        top_tuples = [tuple(row) for row in grid]
                        val = heuristic(top_tuples, target, k)
                        if val < mnh and tuple(top_tuples) not in visited:
                            nxtgrid = top_tuples
                            mnh = val
                        swap(grid, index1, index2)

    top_tuples = [tuple(row) for row in grid]
    top = [list(row) for row in nxtgrid]

    if not (top == grid):
        parent[tuple(nxtgrid)] = (tuple(top_tuples), 0)

    return hillClimber(top, target, k, visited, parent)

def print_path(state_list):
    print("--------------\nOptimal Path: ")
    cnt = 0
    for state in state_list:
        print(f"Move {cnt}:")
        print(state)
        cnt += 1

def swap(arr, index1, index2):
    arr[index1[0]][index1[1]], arr[index2[0]][index2[1]] = arr[index2[0]][index2[1]], arr[index1[0]][index1[1]]

#grid = generate_random_grid()
#grid = [['T2', 'T8', 'T3'], ['T1', 'T6', 'T4'], ['T7', 'B', 'T5']] # for manhatten 
#target = [['T1', 'T2', 'T3'], ['T8', 'B', 'T4'], ['T7', 'T6', 'T5']] #for manhatten 



grid = [['T8', 'T6', 'T5'], ['T7', 'T2', 'T4'], ['T1', 'T3', 'B']]
#grid = [['T5', 'T6', 'T2'], ['B', 'T1', 'T8'], ['T7', 'T4', 'T3']]
target = [['B', 'T6', 'T5'], ['T8', 'T2', 'T4'], ['T7', 'T1', 'T3']]
print("Source:")
for row in grid:
    print(row)

#target = [['T1', 'T2', 'T3'], ['T4', 'T5', 'T6'], ['T7', 'T8', 'B']]

print("Target:")
for row in target:
    print(row)
tp = [tuple(row) for row in grid]

for k in range(2, 4):
    print("--------------\n")
    start = time.time()
    parent = {tuple(tp): ((), -1)}
    visited = set()
    result = hillClimber(grid, target, k, visited, parent)
    end = time.time()

    if result:
        path_list, total_states_explored = result
        print(f"Target state reached using {lst[k]}")
        print_path(path_list)
        print(f"Total states explored: {total_states_explored}")
        print(f"Total number of states in the optimal path: {len(path_list) - 1}")
    else:
        print(f"Target state not reached using {lst[k]}")
        

    print("Time taken for execution:", end - start)
