from graph_data import graph_data
import math

def stj(n):
    permutation = list(range(1, n + 1))
    directions = [-1] * n  # -1 for left, +1 for right

    def largest_mobile_element():
        # Find the largest mobile element (one that can move in its direction)
        largest_mobile = -1
        largest_index = -1
        for i in range(n):
            neighbor_index = i + directions[i]
            if 0 <= neighbor_index < n and permutation[i] > permutation[neighbor_index]:
                if permutation[i] > largest_mobile:
                    largest_mobile = permutation[i]
                    largest_index = i
        return largest_index

    while True:
        yield permutation.copy()  # Output the current permutation

        # Find the largest mobile element
        mobile_index = largest_mobile_element()
        if mobile_index == -1:
            break  # No more mobile elements, permutation generation complete

        swap_index = mobile_index + directions[mobile_index]
        permutation[mobile_index], permutation[swap_index] = permutation[swap_index], permutation[mobile_index]
        directions[mobile_index], directions[swap_index] = directions[swap_index], directions[mobile_index]

        # Reverse the direction of all elements larger than the largest mobile element
        largest_mobile_value = permutation[swap_index]
        for i in range(n):
            if permutation[i] > largest_mobile_value:
                directions[i] *= -1  # Reverse direction

def is_hamiltonian_cycle(path,graph):
    if path[0] != 0 or path[-1] != 0:
        return False
    for i in range(len(path) - 1):
        if path[i + 1] not in graph[path[i]][1]:
            return False
    return True

def find_hamiltonian_cycles(graph):

        n = len(graph) - 1  
        hamiltonian_cycles = []

        for perm in stj(n):
            candidate_path = [0] + perm + [0]  # Start at node 0 and end at node n
            if is_hamiltonian_cycle(candidate_path,graph):
                hamiltonian_cycles.append(candidate_path)
        return hamiltonian_cycles


def calculate_cycle_distance(graph, path):
    distance = 0
    for i in range(len(path) - 1):
        node_a, node_b = graph[path[i]][0], graph[path[i + 1]][0]
        distance += math.sqrt((node_b[0] - node_a[0]) ** 2 + (node_b[1] - node_a[1]) ** 2)
    return distance


def find_optimal_hamiltonian_cycles(graph):
    n = len(graph) - 1  # Exclude start and end nodes
    hamiltonian_cycles = []
    min_distance = float('inf')
    optimal_cycles = []

    # Generate all Hamiltonian cycles
    for perm in stj(n - 1):
        candidate_path = [0] + perm + [n]  # Form a cycle from start to end
        if is_hamiltonian_cycle(candidate_path,graph):
            hamiltonian_cycles.append(candidate_path)
            cycle_distance = calculate_cycle_distance(graph, candidate_path)

            # Check if this cycle is optimal
            if cycle_distance < min_distance:
                min_distance = cycle_distance
                optimal_cycles = [candidate_path]
            elif cycle_distance == min_distance:
                optimal_cycles.append(candidate_path)

    return optimal_cycles, min_distance


if __name__ == '__main__':
    for graph in graph_data:
        print(find_hamiltonian_cycles(graph))