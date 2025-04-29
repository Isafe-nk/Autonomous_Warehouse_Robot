import random
import math
from algorithms import bfs, dijkstra


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obstacle = False
        self.predecessor = None
        self.distance = float("inf")

    def __lt__(self, other):
        return self.distance < other.distance


def create_grid(columns, rows):
    return [[Node(x, y) for x in range(columns)] for y in range(rows)]


def place_start_end(grid):
    rows = len(grid)
    columns = len(grid[0])

    # Randomly select start and end positions
    start_x, start_y = random.randint(0, columns - 1), random.randint(0, rows - 1)
    end_x, end_y = random.randint(0, columns - 1), random.randint(0, rows - 1)

    # Ensure start and end positions are at least 9 units away from each other
    while math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2) < 9:
        start_x, start_y = random.randint(0, columns - 1), random.randint(0, rows - 1)
        end_x, end_y = random.randint(0, columns - 1), random.randint(0, rows - 1)

    start = grid[start_y][start_x]
    end = grid[end_y][end_x]

    return start, end


def generate_obstacles(grid, start, end, obstacle_ratio):
    rows = len(grid)
    columns = len(grid[0])
    obstacles = int(obstacle_ratio * rows * columns)
    reserve_path = bfs(
        grid, start, end, lambda node, clear=False: None
    )  # Expecting BFS to return a set or list of nodes
    if not isinstance(reserve_path, set):
        reserve_path = set(reserve_path)

    while obstacles:
        x, y = random.randint(0, columns - 1), random.randint(0, rows - 1)
        if (
            (x, y) not in [(start.x, start.y), (end.x, end.y)]
            and not grid[y][x].obstacle
            and grid[y][x] not in reserve_path
        ):
            grid[y][x].obstacle = True
            obstacles -= 1


def path_exists(grid, start, end):
    results = {"bfs": None, "dijkstra": None}

    # Run BFS
    results["bfs"] = bool(bfs(grid, start, end, lambda node, clear=False: None))

    # Run Dijkstra
    results["dijkstra"] = bool(dijkstra(grid, start, end, lambda node, clear=False: None))
    return results


def reset_grid(grid):
    for row in grid:
        for node in row:
            node.obstacle = False
            node.predecessor = None
            node.distance = float("inf")

def set_obstacle(grid, x, y, is_obstacle):
    """
    Sets or removes an obstacle at the specified grid cell.

    Args:
        grid (list of list): The grid structure.
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        is_obstacle (bool): True to set as obstacle, False to remove.
    """
    grid[y][x].obstacle = is_obstacle