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
    graph = global_game_data.graph_paths

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
    graph = global_game_data.graph_paths
    start_node = 0
    exit_node = len(graph) - 1

    # helper function in order to facilitate dfs
    def dfs(current, path):
        # base case if path is length 1 or start is the same as exit
        if current == exit_node:
            return path
        # search through all neighbors
        for neighbor in graph[current][1]:
            if neighbor not in path:
                result = dfs(neighbor, path + [neighbor])
                if result is not None:
                    return result
        return None

    path_to_target = dfs(start_node, [start_node])

    full_path = path_to_target
    # assert post condition that target node is hit during full path
    assert global_game_data.target_node in full_path, "failed"
    # assert post condition that they hit exit as the last node
    assert full_path[-1] == exit_node, "failed"
    # for loop to make sure each node hit are neighbors.
    for i in range(len(full_path) - 1):
        current_node = full_path[i]
        next_node = full_path[i + 1]
        assert next_node in graph[current_node][
            1], f" failed:{current_node}{next_node}."

    return full_path


def get_bfs_path():
    graph = global_game_data.graph_paths
    start_node = 0
    exit_node = len(graph) - 1
    queue = deque([[start_node]])
    visited = set()

    while queue:
        path = queue.popleft()
        current = path[-1]

        # Check if we've reached the target node
        if current == global_game_data.target_node:
            path_to_target = path
            break

        if current not in visited:
            visited.add(current)

            for neighbor in graph[current][1]:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    else:
        return None

    queue = deque([[global_game_data.target_node]])
    visited = set()

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == exit_node:
            path_to_exit = path
            break

        if current not in visited:
            visited.add(current)

            for neighbor in graph[current][1]:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    else:
        return None

    full_path = path_to_target[:-1] + path_to_exit
    assert global_game_data.target_node in full_path, "failed"
    assert full_path[-1] == exit_node, "failed"
    for i in range(len(full_path) - 1):
        current_node = full_path[i]
        next_node = full_path[i + 1]
        assert next_node in graph[current_node][
            1], f" failed:{current_node}{next_node}."

    return full_path


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
