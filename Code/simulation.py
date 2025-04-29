import settings
from grid import create_grid, set_obstacle
from algorithms import bfs, dijkstra, reconstruct_path
from gui import draw_path
import random

grid = create_grid(settings.COLUMNS, settings.ROWS)
num_obstacles = 20



def setup_simulation(screen):
    grid = create_grid(settings.COLUMNS, settings.ROWS)
    # Example obstacle setup - This would ideally be dynamic based on user input
    set_obstacle(grid, 10, 10, True)
    set_obstacle(grid, 11, 10, True)
    return grid


def run_pathfinding(grid, start_node, goal_node, screen, algorithm, offset_x=0):
    def visit_callback(node, clear=False):
        pass

    if algorithm == settings.BFS:
        end_node = bfs(grid, start_node, goal_node, visit_callback)
    elif algorithm == settings.DIJKSTRA:
        end_node = dijkstra(grid, start_node, goal_node, visit_callback)

    if end_node:
        path = reconstruct_path(end_node)
        draw_path(
            screen,
            path,
            settings.PATH_COLOR,
            start_node,
            goal_node,
            offset_x,
            algorithm,
            display_info=False,
        )

def toggle_random_obstacles(grid, num_obstacles):
    rows = len(grid)
    columns = len(grid[0])  # Assuming the grid is a 2D list
    for _ in range(num_obstacles):
        while True:  # Keep trying until a valid empty cell is found
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)
            if not grid[y][x].obstacle:  # Only add obstacles to empty cells
                print(f"Adding obstacle at ({x}, {y})")  # Debugging
                set_obstacle(grid, x, y, True)
                break  # Exit the loop once an obstacle is added

print(f"Grid dimensions: {len(grid)} rows, {len(grid[0])} columns")