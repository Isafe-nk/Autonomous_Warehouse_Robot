import pygame
import random
import time
import settings
from grid import create_grid, place_start_end, generate_obstacles, reset_grid
from gui import draw_grid, draw_path, clear_screen, reset_button
from algorithms import bfs, dijkstra
from simulation import toggle_random_obstacles

# Define at the top (global simulation state)
grid_bfs = None
start_bfs = None
end_bfs = None
path_bfs = None
current_position_bfs = None

grid_dijkstra = None
start_dijkstra = None
end_dijkstra = None
path_dijkstra = None
current_position_dijkstra = None

def visualize_path(grid, start, end, screen, offset_x, algo_label, width):
    """Runs one search algorithm, animates its progress, and returns the final path."""
    path = []
    visited_nodes = set()

    def visit_callback(node, clear=False):
        nonlocal path
        if node not in visited_nodes:
            visited_nodes.add(node)
            path.append(node)
            draw_grid(screen, grid, start, end, offset_x)
            draw_path(
                screen,
                path,
                settings.PATH_COLOR,
                start,
                end,
                offset_x,
                algo_label,
            )
            pygame.display.update(pygame.Rect(offset_x, 0, width, settings.SCREEN_HEIGHT))

    # Search
    t0 = time.time()
    if algo_label == settings.BFS:
        shortest_path = bfs(grid, start, end, visit_callback)
    else:
        shortest_path = dijkstra(grid, start, end, visit_callback)
    exec_time = time.time() - t0

    # Draw final path
    if shortest_path:
        clear_screen(screen, offset_x, width)
        draw_grid(screen, grid, start, end, offset_x)
        draw_path(
            screen,
            path,
            settings.VISITED_PATH_COLOR,
            start,
            end,
            offset_x,
            algo_label,
        )
        draw_path(
            screen,
            shortest_path,
            settings.PATH_COLOR,
            start,
            end,
            offset_x,
            algo_label,
            len(path),
            exec_time,
            display_info=True,
        )
        pygame.display.update(pygame.Rect(offset_x, 0, width, settings.SCREEN_HEIGHT))

    return shortest_path

def maybe_add_random_obstacle(grid, chance=1.0):
    if random.random() < chance:
        toggle_random_obstacles(grid, num_obstacles=1)

def run_pathfinding_algorithms(screen):
    """Initializes the grids, computes the initial paths, and visualizes them."""
    global grid_bfs, start_bfs, end_bfs, path_bfs, current_position_bfs
    global grid_dijkstra, start_dijkstra, end_dijkstra, path_dijkstra, current_position_dijkstra

    grid_bfs = create_grid(settings.COLUMNS // 2, settings.ROWS)
    grid_dijkstra = create_grid(settings.COLUMNS // 2, settings.ROWS)

    start_bfs, end_bfs = place_start_end(grid_bfs)
    start_dijkstra, end_dijkstra = (
        grid_dijkstra[start_bfs.y][start_bfs.x],
        grid_dijkstra[end_bfs.y][end_bfs.x],
    )

    generate_obstacles(grid_bfs, start_bfs, end_bfs, settings.OBSTACLE_RATIO)
    for y in range(settings.ROWS):
        for x in range(settings.COLUMNS // 2):
            grid_dijkstra[y][x].obstacle = grid_bfs[y][x].obstacle

    visualize_path(
        grid_bfs,
        start_bfs,
        end_bfs,
        screen,
        10,
        settings.BFS,
        settings.GRID_WIDTH,
    )
    clear_screen(screen, settings.GRID_WIDTH, settings.GRID_WIDTH)
    visualize_path(
        grid_dijkstra,
        start_dijkstra,
        end_dijkstra,
        screen,
        settings.GRID_DISTANCE, 
        settings.DIJKSTRA,
        settings.GRID_WIDTH,
)

    path_bfs = bfs(grid_bfs, start_bfs, end_bfs, visit_callback=lambda node, clear=False: None)
    path_dijkstra = dijkstra(grid_dijkstra, start_dijkstra, end_dijkstra, visit_callback=lambda node, clear=False: None)

    current_position_bfs = start_bfs
    current_position_dijkstra = start_dijkstra

    return grid_bfs, start_bfs, end_bfs, path_bfs, current_position_bfs, grid_dijkstra, start_dijkstra, end_dijkstra, path_dijkstra, current_position_dijkstra

def update_when_button_clicked(screen, grid_bfs, current_position_bfs, end_bfs, path_bfs, grid_dijkstra, current_position_dijkstra, end_dijkstra, path_dijkstra):
    """
    Handles obstacle addition, replanning, and preserves old path if replanning fails.
    """
    maybe_add_random_obstacle(grid_bfs, chance=1.0)
    maybe_add_random_obstacle(grid_dijkstra, chance=1.0)

    # --- BFS Update ---
    if path_bfs and any(grid_bfs[node.y][node.x].obstacle for node in path_bfs):
        print("Obstacle detected in BFS path. Replanning...")
        replanned_path_bfs = bfs(grid_bfs, current_position_bfs, end_bfs, visit_callback=lambda node, clear=False: None)
        if replanned_path_bfs:
            path_bfs = replanned_path_bfs
        else:
            print("No BFS path found anymore! Keeping old path for drawing.")

    if path_bfs and current_position_bfs != end_bfs:
        next_node = path_bfs.pop(0)
        current_position_bfs = next_node

    # --- Dijkstra Update ---
    if path_dijkstra and any(grid_dijkstra[node.y][node.x].obstacle for node in path_dijkstra):
        print("Obstacle detected in Dijkstra path. Replanning...")
        replanned_path_dijkstra = dijkstra(grid_dijkstra, current_position_dijkstra, end_dijkstra, visit_callback=lambda node, clear=False: None)
        if replanned_path_dijkstra:
            path_dijkstra = replanned_path_dijkstra
        else:
            print("No Dijkstra path found anymore! Keeping old path for drawing.")

    if path_dijkstra and current_position_dijkstra != end_dijkstra:
        next_node = path_dijkstra.pop(0)
        current_position_dijkstra = next_node

    # --- Redraw BFS Grid ---
    clear_screen(screen, 10, settings.GRID_WIDTH)
    draw_grid(screen, grid_bfs, start_bfs, end_bfs, 10)

    if path_bfs:
        print("BFS Path:", path_bfs)
        draw_path(screen, path_bfs, settings.PATH_COLOR, current_position_bfs, end_bfs, 10)
        pygame.draw.rect(
            screen, (255, 0, 0),
            (current_position_bfs.x * settings.BLOCK_SIZE + 10,
             current_position_bfs.y * settings.BLOCK_SIZE + 30,
             settings.BLOCK_SIZE,
             settings.BLOCK_SIZE)
        )
    else:
        print("No BFS path to draw.")

    # --- Redraw Dijkstra Grid ---
    clear_screen(screen, settings.GRID_DISTANCE, settings.GRID_WIDTH)
    draw_grid(screen, grid_dijkstra, start_dijkstra, end_dijkstra, settings.GRID_DISTANCE)

    if path_dijkstra:
        draw_path(screen, path_dijkstra, settings.PATH_COLOR, current_position_dijkstra, end_dijkstra, settings.GRID_DISTANCE)
        pygame.draw.rect(
            screen, (255, 0, 0),
            (current_position_dijkstra.x * settings.BLOCK_SIZE + settings.GRID_DISTANCE,
             current_position_dijkstra.y * settings.BLOCK_SIZE + 30,
             settings.BLOCK_SIZE,
             settings.BLOCK_SIZE)
        )
    else:
        print("No Dijkstra path to draw.")

    pygame.display.update()

    return path_bfs, current_position_bfs, path_dijkstra, current_position_dijkstra

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH * 2, settings.SCREEN_HEIGHT + 50))
    pygame.display.set_caption("Pathfinding Algorithms Manual Update")

    font = pygame.font.Font(None, 25)
    button_rect = pygame.Rect(10, settings.SCREEN_HEIGHT + 10, 200, 30)
    update_button_rect = pygame.Rect(220, settings.SCREEN_HEIGHT + 10, 200, 30)

    # Initialize pathfinding
    grid_bfs, start_bfs, end_bfs, path_bfs, current_position_bfs, grid_dijkstra, start_dijkstra, end_dijkstra, path_dijkstra, current_position_dijkstra = run_pathfinding_algorithms(screen)

    running = True
    while running:
        reset_button(screen, button_rect, "Reset", font, (0, 128, 255), (255, 255, 255))
        reset_button(screen, update_button_rect, "Update Obstacles", font, (0, 128, 255), (255, 255, 255))
        pygame.display.update([button_rect, update_button_rect])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    grid_bfs, start_bfs, end_bfs, path_bfs, current_position_bfs, grid_dijkstra, start_dijkstra, end_dijkstra, path_dijkstra, current_position_dijkstra = run_pathfinding_algorithms(screen)
                elif update_button_rect.collidepoint(event.pos):
                    path_bfs, current_position_bfs, path_dijkstra, current_position_dijkstra = update_when_button_clicked(
                        screen, grid_bfs, current_position_bfs, end_bfs, path_bfs, grid_dijkstra, current_position_dijkstra, end_dijkstra, path_dijkstra
                    )

    pygame.quit()


if __name__ == "__main__":
    main()