import graph_data
import global_game_data
from numpy import random
from collections import deque


def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(get_dijkstra_path())


def get_test_path():
    return graph_data.test_path[global_game_data.current_graph_index]


def get_random_path():
    assert graph_data.graph_data, "graph is empty"
    graph = graph_data.graph_data[random.rand(0, 6)]

    start_node = 0
    exit_node = len(graph) - 1

    path = [start_node]
    current = start_node

    while current != exit_node:
        neighbors = graph[current][1]
        if not neighbors:
            return None
        next_node = random.choice(neighbors)
        path.append(next_node)
        current = next_node
        for i in range(len(path) - 1):
            assert path[i + 1] in graph[path[i]][1], "nodes are not connected"

    return path


def get_dfs_path():
    graph = graph_data.graph_data[random.rand(0, 6)]
    start_node = 0
    exit_node = len(graph) - 1

    def dfs(current, path):
        if current == exit_node:
            return path
        for neighbor in graph[current][1]:
            if neighbor not in path:
                result = dfs(neighbor, path + [neighbor])
                if result is not None:
                    return result
        return None

    return dfs(start_node, [start_node])


def get_bfs_path():
    graph = graph_data.graph_data[random.rand(0, 6)]
    start_node = 0
    exit_node = len(graph) - 1
    queue = deque([[start_node]])
    visited = set()

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == exit_node:
            return path

        if current not in visited:
            visited.add(current)
            for neighbor in graph[current][1]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


def get_dijkstra_path():
    graph = graph_data.graph_data[random.rand(0, 6)]
    start_node = 0
    exit_node = len(graph) - 1

    queue = deque([(start_node, [start_node], 0)])
    visited = set()

    while queue:
        current, path, cost = queue.popleft()

        if current == exit_node:
            return path

        if current not in visited:
            visited.add(current)
            for neighbor in graph[current][1]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor], cost + 1))

    return None
