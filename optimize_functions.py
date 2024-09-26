# functions.py

# Python function
optimize_me = """def find_top_students(students, grades):
    # Combine student names with their grades
    student_grades = []
    for i in range(len(students)):
        student_grades.append((students[i], grades[i]))

    # Sort students by their grades in descending order
    for i in range(len(student_grades)):
        for j in range(i + 1, len(student_grades)):
            if student_grades[i][1] < student_grades[j][1]:
                student_grades[i], student_grades[j] = student_grades[j], student_grades[i]

    # Return the top 3 students
    return student_grades[:3]

students = ["Alice", "Bob", "Charlie", "David", "Eve"]
grades = [85, 92, 88, 91, 76]

top_students = find_top_students(students, grades)
print(top_students)"""

# JavaScript function
optimize_me2 = """
function findTopStudents(students, grades) {
    // Combine student names with their grades
    let studentGrades = [];
    for (let i = 0; i < students.length; i++) {
        studentGrades.push([students[i], grades[i]]);
    }

    // Sort students by their grades in descending order
    for (let i = 0; i < studentGrades.length; i++) {
        for (let j = i + 1; j < studentGrades.length; j++) {
            if (studentGrades[i][1] < studentGrades[j][1]) {
                [studentGrades[i], studentGrades[j]] = [studentGrades[j], studentGrades[i]];
            }
        }
    }

    // Return the top 3 students
    return studentGrades.slice(0, 3);
}

let students = ["Alice", "Bob", "Charlie", "David", "Eve"];
let grades = [85, 92, 88, 91, 76];

let topStudents = findTopStudents(students, grades);
console.log(topStudents);
"""

# Python function
optimize_me3 = """
def sum_elements(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total

numbers = [1, 2, 3, 4, 5, 6]
print(sum_elements(numbers))
"""
# Python function
optimize_me4 = """
def find_primes(n):
    primes = []
    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, i):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

n = 50
print(find_primes(n))
"""
# JavaScript function
optimize_me5 = """
function sumElements(numbers) {
    let total = 0;
    for (let i = 0; i < numbers.length; i++) {
        total += numbers[i];
    }
    return total;
}

let numbers = [1, 2, 3, 4, 5, 6];
console.log(sumElements(numbers));
"""

# JavaScript function
optimize_me6 = """
def find_primes(n):
    primes = []
    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

n = 50
print(find_primes(n))
"""

# Python function
optimize_me7 = """
def process_data(data):
    result = []
    
    # Step 1: Remove duplicates by checking every element
    for i in range(len(data)):
        found_duplicate = False
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                found_duplicate = True
                break
        if not found_duplicate:
            result.append(data[i])

    # Step 2: Sort the data using bubble sort
    for i in range(len(result)):
        for j in range(0, len(result) - i - 1):
            if result[j] > result[j + 1]:
                temp = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temp

    # Step 3: Square each number if it's even, cube if it's odd
    final_result = []
    for num in result:
        if num % 2 == 0:
            final_result.append(num ** 2)
        else:
            final_result.append(num ** 3)
    
    # Step 4: Check if any number in the final_result is greater than 1000
    for num in final_result:
        if num > 1000:
            print("Found a large number:", num)
    
    return final_result
"""
# Recursive path finding
#
optimize_me8 = """
def path_finder(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # Step 1: Initialize a list of all possible paths from (0,0) to (rows-1,cols-1)
    all_paths = []
    
    def find_paths(x, y, current_path):
        if x == rows - 1 and y == cols - 1:
            all_paths.append(current_path + [(x, y)])
            return
        
        if x < rows - 1:
            find_paths(x + 1, y, current_path + [(x, y)])
        
        if y < cols - 1:
            find_paths(x, y + 1, current_path + [(x, y)])
    
    find_paths(0, 0, [])
    
    # Step 2: Evaluate the sum of values along each path
    best_path = None
    best_sum = float('-inf')
    
    for path in all_paths:
        current_sum = 0
        for (x, y) in path:
            current_sum += grid[x][y]
        
        if current_sum > best_sum:
            best_sum = current_sum
            best_path = path
    
    # Step 3: Return the path with the highest sum and the sum itself
    return best_path, best_sum
"""

# Here's a more complicated pathfinding task that involves obstacles,
# weights, and diagonally permissible movements.

# You can move in 8 possible directions (up, down, left, right, and the 4 diagonals),
# and the task is to find the minimum cost path from the top-left corner (0,0) to the bottom-right corner
# (rows-1, cols-1), avoiding obstacles.
optimize_me9 = """
import heapq

def find_min_cost_path(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # Directions: up, down, left, right, and diagonals
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # DP table to store the minimum cost to reach each cell
    min_cost = [[float('inf')] * cols for _ in range(rows)]
    min_cost[0][0] = grid[0][0]
    
    # Priority queue (min-heap) to keep track of the minimum cost paths
    pq = [(grid[0][0], 0, 0)]  # (cost, row, col)
    
    while pq:
        current_cost, x, y = heapq.heappop(pq)
        
        # If we've reached the bottom-right corner, return the cost
        if x == rows - 1 and y == cols - 1:
            return current_cost
        
        # Skip this cell if we've already found a better way
        if current_cost > min_cost[x][y]:
            continue
        
        # Explore all 8 possible directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] > 0:
                new_cost = current_cost + grid[nx][ny]
                
                # If a cheaper path to (nx, ny) is found, update and push to the heap
                if new_cost < min_cost[nx][ny]:
                    min_cost[nx][ny] = new_cost
                    heapq.heappush(pq, (new_cost, nx, ny))
    
    # If we finish and haven't reached the bottom-right corner, there's no valid path
    return -1
"""

optimize_me10 = """
import heapq

# Define movement costs for moving in the grid
MOVEMENT_COST = {
    'horizontal': 1,  # moving left/right in a row
    'depth': 1,       # moving forward/backward in a channel
    'vertical': 2     # moving up/down between levels (more expensive)
}

# Directions: left, right, forward (depth), backward, up, down
DIRECTIONS = [
    (0, 1, 0),  # right
    (0, -1, 0), # left
    (1, 0, 0),  # forward (depth)
    (-1, 0, 0), # backward (depth)
    (0, 0, 1),  # up
    (0, 0, -1)  # down
]

def heuristic(a, b):
    #Heuristic function for A* (Manhattan distance in 3D).
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def find_fastest_route(warehouse, start, goal):
    rows, cols, levels = len(warehouse), len(warehouse[0]), len(warehouse[0][0])
    pq = []
    heapq.heappush(pq, (0, start))  # (cost, (x, y, z))
    costs = {start: 0}
    came_from = {start: None}
    
    while pq:
        current_cost, current = heapq.heappop(pq)
        
        if current == goal:
            break
        
        x, y, z = current
        for dx, dy, dz in DIRECTIONS:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            # Check if the next move is within bounds
            if 0 <= nx < rows and 0 <= ny < cols and 0 <= nz < levels:
                if warehouse[nx][ny][nz] == 1:  # obstacle (other rolls)
                    continue
                
                # Determine the cost for this move
                if dx != 0 or dy != 0:  # Horizontal or depth movement
                    new_cost = current_cost + MOVEMENT_COST['horizontal'] if dz == 0 else MOVEMENT_COST['depth']
                else:  # Vertical movement
                    new_cost = current_cost + MOVEMENT_COST['vertical']
                
                # If this new path is cheaper, take it
                if (nx, ny, nz) not in costs or new_cost < costs[(nx, ny, nz)]:
                    costs[(nx, ny, nz)] = new_cost
                    priority = new_cost + heuristic((nx, ny, nz), goal)
                    heapq.heappush(pq, (priority, (nx, ny, nz)))
                    came_from[(nx, ny, nz)] = current
    
    # Reconstruct the path from 'start' to 'goal'
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    
    return path, costs[goal] if goal in costs else float('inf')

# Example usage
warehouse = [
    # 3D grid where 0 is free space and 1 is an obstacle
    # Layer 0 (ground level)
    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[0, 0, 0], [1, 1, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    
    # Layer 1 (above ground)
    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[0, 0, 0], [1, 1, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
]

start = (0, 0, 0)  # Starting position (ground level, row 0, column 0)
goal = (2, 2, 0)   # Target position (ground level, row 2, column 2)

path, cost = find_fastest_route(warehouse, start, goal)
print("Optimal Path:", path)
print("Total Cost:", cost)
"""
