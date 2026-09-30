import collections

# The warehouse map provided in the specification
WAREHOUSE_MAP = [
    "#####################",
    "#......#..G#........#",
    "#.##.....##########..#",
    "#S....#..#....##....#",
    "#.######.###.#.###..#",
    "#.......#........#..#",
    "#####################"
]

class WarehouseAgent:
    def __init__(self, grid):
        self.grid = [list(row) for row in grid]
        self.rows = len(grid)
        self.cols = max(len(row) for row in grid)
        self.start = None
        self.goal = None
        
        # Locate Start (S) and Goal (G)
        for r in range(self.rows):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal = (r, c)

    def get_neighbors(self, r, c):
        """Return valid adjacent moves: Up, Down, Left, Right"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < len(self.grid[nr]):
                if self.grid[nr][nc] != '#':
                    neighbors.append((nr, nc))
        return neighbors

    def find_path(self):
        """Uses Breadth-First Search to find the shortest collision-free path."""
        if not self.start or not self.goal:
            return None

        queue = collections.deque([[self.start]])
        visited = set([self.start])

        while queue:
            path = queue.popleft()
            curr_r, curr_c = path[-1]

            if (curr_r, curr_c) == self.goal:
                return path

            for nr, nc in self.get_neighbors(curr_r, curr_c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    new_path = list(path)
                    new_path.append((nr, nc))
                    queue.append(new_path)

        return None

    def print_path(self, path):
        """Prints the grid with the path marked as '*'."""
        if not path:
            print("No path exists.")
            return
            
        display_grid = [row[:] for row in self.grid]
        for r, c in path:
            if display_grid[r][c] not in ('S', 'G'):
                display_grid[r][c] = '*'
                
        for row in display_grid:
            print("".join(row))

if __name__ == "__main__":
    agent = WarehouseAgent(WAREHOUSE_MAP)
    print("Searching for a collision-free path...")
    solution = agent.find_path()
    agent.print_path(solution)