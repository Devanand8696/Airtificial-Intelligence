import random
import heapq

# Function to generate a random grid with shuffled elements
def generate_random_grid():
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', 'B']
    random.shuffle(chars)
    r_grid = [chars[i:i+3] for i in range(0, 9, 3)]
    return r_grid

# Function to get possible next states from a given state
def get_next_states(state):
    n = len(state)
    next_states = []
    
    for i in range(n):
        for j in range(n):
            if state[i][j] == 'B':
                x, y = i, j
                moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for dx, dy in moves:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < n and 0 <= new_y < n:
                        next_state = [list(row) for row in state]
                        next_state[x][y], next_state[new_x][new_y] = next_state[new_x][new_y], next_state[x][y]
                        next_states.append(tuple(map(tuple, next_state)))
        
    return next_states

# Uniform Cost Search algorithm to find a path from a start state to a target state
def uniform_cost_search(start_state, target_state):
    visited = set()
    priority_queue = [(0, start_state, None)]
    parent_map = {}  # To keep track of the parent state

    while priority_queue:
        cost, current_state, parent = heapq.heappop(priority_queue)
        if current_state == target_state:
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parent_map.get(current_state)
            path.reverse()
          
            return cost, path
        visited.add(current_state)
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                heapq.heappush(priority_queue, (cost + 1, next_state, current_state))
                parent_map[next_state] = current_state
    
    return -1, []

def  iterative_deepening_search(start_state, target_state):
    depth = 0
    while True:
        stack = [(start_state, 0, None)]
        visited = set()
        parent_map = {}  # To keep track of the parent state
        while stack:
            current_state, cost, parent = stack.pop()
            if current_state == target_state:
                path = []
                while current_state is not None:
                    path.append(current_state)
                    current_state = parent_map.get(current_state)
                path.reverse()
                return cost, path
            visited.add(current_state)
            if cost < depth:
                for next_state in get_next_states(current_state):
                    if next_state not in visited:
                        stack.append((next_state, cost + 1, current_state))
                        parent_map[next_state] = current_state
        depth += 1
    return -1,[]

# Grid initialization
#start_grid = generate_random_grid()
start_grid = [['2', '7', '4'], ['5', '3', '1'], ['8', '6', 'B']]
target_grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', 'B']]

# Call the search algorithms


ucs_cost, ucs_path = uniform_cost_search(tuple(map(tuple, start_grid)), tuple(map(tuple, target_grid)))
ids_cost, ids_path = iterative_deepening_search(tuple(map(tuple, start_grid)), tuple(map(tuple, target_grid)))

# Print results
if ucs_cost == -1:
    print("Uniform Cost Search: Not reachable")
else:
    print("Uniform Cost Search: Found a path to the target grid. Cost:", ucs_cost)
    print("UCS Path:")
    for p in ucs_path:
        for row in p:
            print(row)
            
print( )
if ids_cost == -1:
    print("Iterative Deepening Search: Not reachable")
else:
    print("Iterative Deepening Search: Found a path to the target grid. Cost:", ids_cost)
    print("IDS Path:")
    for p in ids_path:
        for row in p:
            print(row)
        print()
