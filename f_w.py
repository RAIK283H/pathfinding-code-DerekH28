

import global_game_data
import graph_data


def floyd_warshall():
    graph = graph_data.graph_data[global_game_data.current_graph_index]  # Dynamically retrieve the graph
    n = len(graph)  # Number of nodes in the graph
    dist = [[float('inf')] * n for _ in range(n)]  # Initialize distance matrix
    parent = [[None] * n for _ in range(n)]       # Initialize parent matrix

    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    parent[i][j] = parent[k][j]  # Update the parent matrix

    def get_path(start, end):
        """
        Retrieve the shortest path from start to end.
        :param start: Starting node
        :param end: Ending node
        :return: List representing the path from start to end, or None if no path exists
        """
        if parent[start][end] is None:
            return None  # No path exists
        path = []
        while end is not None:
            path.append(end)
            end = parent[start][end]
        return path[::-1]  # Reverse the path to get start to end

    return dist, get_path  # Return distance matrix and the path retrieval function

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5
