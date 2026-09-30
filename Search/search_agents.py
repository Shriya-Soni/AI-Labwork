import heapq
import collections
import math

# ==========================================
# WAREHOUSE MAPS FOR TESTING
# ==========================================

MAP_ORIGINAL = [
    "#################",
    "#S....#.......#.#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#........G....#.#",
    "#################"
]

MAP_TRIVIAL = [
    "#####",
    "#SG##",
    "#####"
]

MAP_NO_SOLUTION = [
    "#######",
    "#S....#",
    "###.###",
    "#...#G#",
    "#######"
]

MAP_ALT_PATHS = [
    "#######",
    "#S....#",
    "#.###.#",
    "#....G#",
    "#######"
]

# ==========================================
# SEARCH AGENT & ALGORITHMS
# ==========================================

class SearchAgent:
    def __init__(self, grid):
        self.grid = [list(row) for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = None
        self.goal = None
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal = (r, c)

    def get_neighbors(self, state):
        r, c = state
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Up, Down, Left, Right
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

    def print_path(self, path):
        if not path:
            print("No path to print.")
            return
        temp_grid = [row[:] for row in self.grid]
        for r, c in path:
            if temp_grid[r][c] not in ('S', 'G'):
                temp_grid[r][c] = '*'
        for row in temp_grid:
            print("".join(row))

# --- HEURISTICS ---
def h_manhattan(state, goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def h_zero(state, goal):
    return 0

def h_euclidean(state, goal):
    return math.sqrt((state[0] - goal[0])**2 + (state[1] - goal[1])**2)

def h_multiplied(state, goal):
    return 2 * (abs(state[0] - goal[0]) + abs(state[1] - goal[1]))

# --- A* SEARCH ---
def a_star_search(agent, heuristic_func=h_manhattan):
    if not agent.start or not agent.goal:
        return None, 0
    
    frontier = []
    # (f_score, tie_breaker, state, path)
    heapq.heappush(frontier, (0, 0, agent.start, [agent.start]))
    
    g_score = {agent.start: 0}
    states_expanded = 0
    tie_breaker = 1
    
    while frontier:
        f, _, current, path = heapq.heappop(frontier)
        
        if current == agent.goal:
            return path, states_expanded
            
        states_expanded += 1
        
        for neighbor in agent.get_neighbors(current):
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                h = heuristic_func(neighbor, agent.goal)
                f_score = tentative_g + h
                
                new_path = list(path)
                new_path.append(neighbor)
                
                heapq.heappush(frontier, (f_score, tie_breaker, neighbor, new_path))
                tie_breaker += 1
                
    return None, states_expanded

# --- BREADTH-FIRST SEARCH ---
def bfs_search(agent):
    if not agent.start or not agent.goal:
        return None, 0
        
    frontier = collections.deque([(agent.start, [agent.start])])
    visited = {agent.start}
    states_expanded = 0
    
    while frontier:
        current, path = frontier.popleft()
        
        if current == agent.goal:
            return path, states_expanded
            
        states_expanded += 1
        
        for neighbor in agent.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                frontier.append((neighbor, new_path))
                
    return None, states_expanded


# ==========================================
# EXECUTION & TESTING SCRIPT
# ==========================================
if __name__ == "__main__":
    maps = {
        "Test 1: Original Warehouse": MAP_ORIGINAL,
        "Test 2: Trivial Case": MAP_TRIVIAL,
        "Test 3: No Solution": MAP_NO_SOLUTION,
        "Test 4: Alternative Paths": MAP_ALT_PATHS
    }

    print("=== TASK 3: SYSTEMATIC TESTING (A* with Manhattan) ===")
    for name, grid in maps.items():
        agent = SearchAgent(grid)
        path, expanded = a_star_search(agent, h_manhattan)
        print(f"\n{name}")
        if path:
            print(f"Path found! Length: {len(path)-1} | States Expanded: {expanded}")
            if name != "Test 3: No Solution":
                agent.print_path(path)
        else:
            print(f"No solution found. States Expanded: {expanded}")


    print("\n=== TASK 5: A* vs BFS COMPARISON (Original Map) ===")
    agent_orig = SearchAgent(MAP_ORIGINAL)
    
    path_bfs, exp_bfs = bfs_search(agent_orig)
    len_bfs = len(path_bfs)-1 if path_bfs else "N/A"
    
    path_astar, exp_astar = a_star_search(agent_orig, h_manhattan)
    len_astar = len(path_astar)-1 if path_astar else "N/A"
    
    print(f"{'Measure':<20} | {'BFS':<10} | {'A*':<10}")
    print("-" * 45)
    print(f"{'Solution found':<20} | {str(path_bfs is not None):<10} | {str(path_astar is not None):<10}")
    print(f"{'Path length':<20} | {len_bfs:<10} | {len_astar:<10}")
    print(f"{'States expanded':<20} | {exp_bfs:<10} | {exp_astar:<10}")


    print("\n=== TASK 6: HEURISTIC INVESTIGATION (Original Map) ===")
    heuristics = {
        "Manhattan (Standard)": h_manhattan,
        "h(n) = 0 (Uniform Cost)": h_zero,
        "Euclidean": h_euclidean,
        "h(n) * 2 (Inadmissible)": h_multiplied
    }
    
    print(f"{'Heuristic':<25} | {'Solution?':<10} | {'Path Len':<10} | {'Expanded'}")
    print("-" * 60)
    for h_name, h_func in heuristics.items():
        path_h, exp_h = a_star_search(agent_orig, h_func)
        l_h = len(path_h)-1 if path_h else "N/A"
        sol = "Yes" if path_h else "No"
        print(f"{h_name:<25} | {sol:<10} | {l_h:<10} | {exp_h}")