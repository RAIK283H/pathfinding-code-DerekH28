import heapq

import graph_data
import global_game_data
import f_w
from numpy import random
from collections import deque


def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(f_w.floyd_warshall())


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
    print(full_path)
    return full_path



def get_dijkstra_path():
        graph = graph_data.graph_data[global_game_data.current_graph_index]
        start_node = 0  # Start node
        exit_node = len(graph) - 1  # Exit node

        def calculate_distance(point1, point2):
            return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5
        # Priority queue and distance tracking
        pq = []
        heapq.heappush(pq,(0, start_node))
        distances = {i: float('inf') for i in range(len(graph))}
        distances[start_node] = 0
        parents = {start_node: None}  # Track parents for path reconstruction

        while pq:
            current_distance, current_index = heapq.heappop(pq)
            current_index = int(current_index)


            # If we reached the exit node, reconstruct the path
            if current_index == exit_node:
                path = []
                while current_index is not None:
                    path.append(current_index)
                    current_index = parents[current_index]
                path.reverse()  # Reverse path to start from the start node
                return path

            # Explore neighbors and update distances
            for neighbor_index in graph[current_index][1]:
                neighbor_distance = current_distance + calculate_distance(graph[current_index][0],
                graph[neighbor_index][0])

                if neighbor_distance < distances[neighbor_index]:
                    distances[neighbor_index] = neighbor_distance
                    parents[neighbor_index] = current_index
                    heapq.heappush(pq,(neighbor_distance, neighbor_index))

        return None
