from collections import deque
import heapq


def bfs(grid, start, end, visit_callback):
    """
    Perform a Breadth-First Search (BFS) on a grid to find the shortest path.

    Parameters:
        grid (list of list): The 2D grid representing the environment.
        start (Node): The starting node for the search.
        end (Node): The target node to reach.
        visit_callback (function): A callback function to visualize or process visited nodes.

    Returns:
        list: A list of nodes representing the shortest path from start to end, or an empty list if no path exists.
    """
    queue = deque([start])
    visited = set([start])
    visit_callback(start, clear=True)

    while queue:
        current_node = queue.popleft()
        visit_callback(current_node)

        if current_node == end:
            return reconstruct_path(current_node)

        for neighbor in get_neighbors(grid, current_node):
            if neighbor not in visited and not neighbor.obstacle:
                visited.add(neighbor)
                neighbor.predecessor = current_node
                queue.append(neighbor)
    return []


def dijkstra(grid, start, end, visit_callback):
    queue = []
    heapq.heappush(queue, (0, start))
    start.distance = 0
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue

        visit_callback(current_node)
        visited.add(current_node)

        if current_node == end:
            return reconstruct_path(current_node)

        for neighbor in get_neighbors(grid, current_node):
            if neighbor not in visited and not neighbor.obstacle:
                new_distance = current_distance + 1
                if new_distance < neighbor.distance:
                    neighbor.distance = new_distance
                    neighbor.predecessor = current_node
                    heapq.heappush(queue, (new_distance, neighbor))

    return []


def get_neighbors(grid, node):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    neighbors = []
    max_x, max_y = len(grid[0]), len(grid)
    for dx, dy in directions:
        x, y = node.x + dx, node.y + dy
        if 0 <= x < max_x and 0 <= y < max_y:
            neighbors.append(grid[y][x])
    return neighbors


def reconstruct_path(end_node):
    if not end_node:
        return []  # No path found

    path = []
    current = end_node
    while current:
        path.append(current)
        current = current.predecessor  # Follow the predecessor chain
    path.reverse()  # Reverse to start from the beginning
    return path
