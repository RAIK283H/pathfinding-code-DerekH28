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
    #global_game_data.graph_paths.append(get_dijkstra_path())


def get_test_path():
    return graph_data.test_path[global_game_data.current_graph_index]


def get_random_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]

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
    path.remove(0)
    print(path)
    return path



def get_dfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]

    start_node = 0
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    exit_node = len(graph) - 1

    # helper function in order to facilitate dfs

    def dfs(current, path):
        # base case if path is length 1 or start is the same as exit
        if current == target_node:
            return path
        # search through all neighbors
        for neighbor in graph[current][1]:
            if neighbor not in path:
                result = dfs(neighbor, path + [neighbor])
                if result is not None:
                    return result
        return None

    path_to_target = dfs(start_node, [start_node])


    if not path_to_target or path_to_target[-1] != target_node:
        return None  # If no path to the target node, return None


    def dfs_exit(current_index, path):
        if current_index == exit_node:  # Now we check if we reached the exit node
            return path  # Return the path once we hit the exit node

        neighbors = graph[current_index][1]
        for neighbor in neighbors:  # Navigate using neighbor indices
            if neighbor not in path:
                result = dfs_exit(neighbor, path + [neighbor])
                if result is not None:
                    return result
        return None

    path_to_exit = dfs_exit(target_node, [target_node])

    full_path = path_to_target[:-1] + path_to_exit

    assert target_node in full_path, "failed1"
    # assert post condition that they hit exit as the last node
    for i in range(len(full_path) - 1):
        current_node = full_path[i]
        next_node = full_path[i + 1]
        assert next_node in graph[current_node][
            1], f" failed2:{current_node}{next_node}."
    full_path.remove(0)
    print(full_path)
    return full_path


def get_bfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start_node = 0
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    exit_node = len(graph) - 1

    def bfs_path(graph, start, goal_node):

        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            current_index = path[-1]

            if current_index == goal_node:
                return path

            # If the current node hasn't been visited yet
            if current_index not in visited:
                visited.add(current_index)  # Mark the current node index as visited

                # Iterate over neighbors
                neighbors = graph[current_index][1]  # Get neighbors list
                for neighbor_index in neighbors:
                    if neighbor_index not in visited:  # Only consider unvisited neighbors
                        new_path = list(path)  # Create a new path that includes the neighbor
                        new_path.append(neighbor_index)  # Append the neighbor to the path
                        queue.append(new_path)  # Add the new path to the queue
            current_index = path[-1]

        return None
    path_to_target = bfs_path(graph, start_node, target_node)
    if path_to_target is None:
        return None

    # Second BFS: Find path from target_node to exit_node
    path_to_exit = bfs_path(graph, target_node, exit_node)
    if path_to_exit is None:
        return None

    # Concatenate the paths, removing the duplicate target node from the second path
    full_path = path_to_target[:-1] + path_to_exit
    full_path.remove(0)
    print(full_path)
    return full_path



def get_dijkstra_path():
    # graph = graph_data.graph_data[random.rand(0, 6)]
    # start_node = 0
    # exit_node = len(graph) - 1
    #
    # queue = deque([(start_node, [start_node], 0)])
    # visited = set()
    #
    # while queue:
    #     current, path, cost = queue.popleft()
    #
    #     if current == exit_node:
    #         return path
    #
    #     if current not in visited:
    #         visited.add(current)
    #         for neighbor in graph[current][1]:
    #             if neighbor not in visited:
    #                 queue.append((neighbor, path + [neighbor], cost + 1))

    return None
