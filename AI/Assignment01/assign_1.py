import random
from collections import deque
# Function to generate a random grid with shuffled elements
def generate_random_grid():
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', 'B']
    random.shuffle(chars)
    r_grid = [chars[i:i+3] for i in range(0, 9, 3)]
    return r_grid

# Breadth-First Search algorithm to find a path from a given grid to the target grid
def bfs(grid, target):
    n = len(grid)
    visited = set()
    queue = deque()
    top_tuples = [tuple(row) for row in grid]
    queue.append(tuple(top_tuples))
    
    while queue:
        top = [list(row) for row in queue.popleft()]
        top_tuples = [tuple(row) for row in top]
        visited.add(tuple(top_tuples))
        #if target found 
        if top == target:
            print("BFS: Found a path to the target grid. Visited:", len(visited))
            return 1
         # Find the position of 'B' (blank space)
        for i in range(3):
            for j in range(3):
                if top[i][j] == 'B':
                    x, y = i, j
        #moves possibility and appending if not visited
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dx, dy in moves:
            if 0 <= x + dx < n and 0 <= y + dy < n:
                index1 = (x, y)
                index2 = (x + dx, y + dy)
                swap(top, index1, index2)
                top_tuples = [tuple(row) for row in top]
                if tuple(top_tuples) not in visited:
                    queue.append(tuple(top_tuples))
                swap(top, index1, index2)
     #return -1 if target not found             
    return -1  
def dfs(grid,target):
    count=0
    n=len(grid)
    #using set for checking the different grids we arrived at
    visited =set()
    #print(visited[0]);
    stack=[]
    top_tuples = [tuple(row) for row in grid]
    stack.append(tuple(top_tuples))
    while(len(stack)):
      #print(count)
      top=[list(row) for row in stack[-1]]
      top_tuples = [tuple(row) for row in top]
      visited.add(tuple(top_tuples))
      pop_element = True
      #if target is found
      if(top==target):
          print("DFS: Found a path to the target grid. Visited:",len(visited))
          return 1
      #find the position of blank letter B
      for i in range (3):
          for j in range (3):
              if(top[i][j]=='B'):
                  x,y=i,j
        #order of dfs is left right up down
      if(y-1>=0 and pop_element):
            index1=(x,y)
            index2=(x,y-1)
            swap(top,index1,index2)
            top_tuples = [tuple(row) for row in top]
            #checking if tuple is already visited or not
            if(tuple(top_tuples) not in visited):
              stack.append(tuple(top_tuples))
              pop_element = False
            swap(top,index1,index2)
      if(y+1<n and pop_element):
            index1=(x,y)
            index2=(x,y+1)
            swap(top,index1,index2)
            top_tuples = [tuple(row) for row in top]
            if(tuple(top_tuples) not in visited):
              stack.append(tuple(top_tuples))
              pop_element = False
            swap(top,index1,index2)
      if(x-1>=0 and pop_element):
            index1=(x,y)
            index2=(x-1,y)
            swap(top,index1,index2)
            top_tuples = [tuple(row) for row in top]
            if(tuple(top_tuples) not in visited):
              stack.append(tuple(top_tuples))
              pop_element = False
            swap(top,index1,index2)
            
      if(x+1<n and pop_element):
            index1=(x,y)
            index2=(x+1,y)
            swap(top,index1,index2)
            top_tuples = [tuple(row) for row in top]
            if(tuple(top_tuples) not in visited):
              stack.append(tuple(top_tuples))
              pop_element = False
            swap(top,index1,index2)
      
      #if atleast 1 diff state is reachable then we donot pop
      if(pop_element):
          stack.pop()
          #count and len of visted are same
      count+=1
    return -1

def swap(arr, index1, index2):
    arr[index1[0]][index1[1]], arr[index2[0]][index2[1]] = arr[index2[0]][index2[1]], arr[index1[0]][index1[1]]


grid = generate_random_grid()
#grid=[['2','7','4'],['5','3','1'],['8','6','B']]
print("Source:")
for row in grid:
    print(row)
target = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', 'B']]

result = bfs(grid, target)
if result == -1:
    print(" BFS:Not reachable")
    
result=dfs(grid,target)
if result == -1:
    print(" DFS:Not reachable")
