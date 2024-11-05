import math
import unittest
from unittest.mock import patch
import permutations
import pathing


class TestPathFinding(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('test'.upper(), 'TEST')

    def test_isupper(self):
        self.assertTrue('TEST'.isupper())
        self.assertFalse('Test'.isupper())

    def test_floating_point_estimation(self):
        first_value = 0
        for x in range(1000):
            first_value += 1/100
        second_value = 10
        almost_pi = 3.1
        pi = math.pi
        self.assertNotEqual(first_value,second_value)
        self.assertAlmostEqual(first=first_value,second=second_value,delta=1e-9)
        self.assertNotEqual(almost_pi, pi)
        self.assertAlmostEqual(first=almost_pi, second=pi, delta=1e-1)

    @patch('global_game_data.graph_paths', [
        # Mock graph with (x, y) coordinates and neighbor indices
        [(0, 0), [1]],  # Node (0,0) with neighbor [1]
        [(200, -200), [0, 2]],  # Node (200,-200) with neighbors [0, 2]
        [(200, -400), [1]]  # Node (200,-400) with neighbor [1]
    ])
    @patch('global_game_data.target_node', 1)
    def test_dfs_path(self):
        # Mock global_game_data and test the DFS function
        start_node = 0
        target_node = 1  # Assuming the target is node 1
        exit_node = 2  # Exit node is 2

        expected_path = [0, 1, 2]  # Expected path through (0,0) -> (200,-200) -> (200,-400)
        path = pathing.get_dfs_path()
        self.assertEqual(path, expected_path, "DFS path should hit target node 1 before reaching exit.")

    @patch('global_game_data.graph_paths', [
        [(0, 0), [1]],
        [(200, -200), [0, 2]],
        [(200, -400), [1]]
    ])
    @patch('global_game_data.target_node', 1)
    def test_bfs_path(self):
        # Mock global_game_data and test the BFS function
        start_node = 0
        target_node = 1  # Assuming the target is node 1
        exit_node = 2  # Exit node is 2

        expected_path = [0, 1, 2]  # Expected path through (0,0) -> (200,-200) -> (200,-400)
        path = pathing.get_bfs_path()
        self.assertEqual(path, expected_path, "BFS path should hit target node 1 before reaching exit.")

    @patch('global_game_data.graph_paths', [
        # More complex graph with multiple paths and (x, y) coordinates
        [(0, 0), [1, 2]],  # Node (0,0) with neighbors [1, 2]
        [(50, -200), [0, 3]],  # Node (50,-200) with neighbors [0, 3]
        [(50, -300), [0, 3]],  # Node (50,-300) with neighbors [0, 3]
        [(200, -500), [1, 2]]  # Node (200,-500) with neighbors [1, 2]
    ])
    @patch('global_game_data.target_node', 1)
    def test_multiple_paths(self):
        # Test case where multiple paths exist; ensure it hits the target first
        expected_dfs_path = [0, 1, 3]  # Expected DFS path through (0,0) -> (50,-200) -> (200,-500)
        path = pathing.get_dfs_path()
        self.assertEqual(path, expected_dfs_path, "DFS should return the correct path hitting target first.")

        expected_bfs_path = [0, 1, 3]  # Expected BFS path through (0,0) -> (50,-200) -> (200,-500)
        path = pathing.get_bfs_path()
        self.assertEqual(path, expected_bfs_path, "BFS should return the correct path hitting target first.")

    def test_number_of_permutations(self):
        """Test that the number of permutations generated is correct for a given n."""
        n = 4
        expected_permutations = math.factorial(n)
        generated_permutations = list(permutations.stj(n))
        self.assertEqual(len(generated_permutations), expected_permutations,
                         f"Expected {expected_permutations} permutations, got {len(generated_permutations)}")

    def test_permutation_uniqueness(self):
        """Test that all generated permutations are unique."""
        n = 4
        generated_permutations = list(permutations.stj(n))
        unique_permutations = set(tuple(p) for p in generated_permutations)
        self.assertEqual(len(generated_permutations), len(unique_permutations), "Generated permutations are not unique")

    def test_permutation_contents(self):
        """Test that each permutation is a rearrangement of the numbers from 1 to n."""
        n = 4
        generated_permutations = list(permutations.stj(n))
        expected_elements = set(range(1, n + 1))
        for perm in generated_permutations:
            self.assertEqual(set(perm), expected_elements, f"Permutation {perm} does not contain the correct elements")

    def test_permutation_order_for_small_n(self):
        """Verify known order of permutations for small n values (e.g., n=3)."""
        n = 3
        generated_permutations = list(permutations.stj(n))
        expected_permutations = [
            [1, 2, 3],
            [1, 3, 2],
            [3, 1, 2],
            [3, 2, 1],
            [2, 3, 1],
            [2, 1, 3]
        ]
        self.assertEqual(generated_permutations, expected_permutations,
                         f"Permutations for n={n} do not match expected order")
    def test_single_hamiltonian_cycle(self):
        """Test a graph with a single Hamiltonian cycle."""
        # Define a small graph with a single Hamiltonian cycle: 0 -> 1 -> 2 -> 3 -> 0
        graph = [
            [(0, 0), [1, 0]],  # Node 0 connected to Nodes 1 and 2
            [(2, 2), [0, 1]]  # Node 2 connected to Nodes 0 and 1
        ]
        cycles = permutations.find_hamiltonian_cycles(graph)
        expected_cycles = [[0, 1, 0]]
        self.assertEqual(cycles, expected_cycles, "Should find a single Hamiltonian cycle")

    def test_multiple_hamiltonian_cycles(self):
        """Test a graph with multiple Hamiltonian cycles."""
        # Define a graph with two Hamiltonian cycles: 0 -> 1 -> 2 -> 3 -> 0 and 0 -> 3 -> 2 -> 1 -> 0
        graph = [
            [(0, 0), [1, 3]],       # Node 0 connected to 1 and 3
            [(1, 1), [0, 2]],       # Node 1 connected to 0 and 2
            [(2, 2), [1, 3]],       # Node 2 connected to 1 and 3
            [(3, 3), [2, 0]],       # Node 3 connected to 2 and 0
        ]
        cycles = permutations.find_hamiltonian_cycles(graph)
        expected_cycles = [[0, 1, 2, 3, 0], [0, 3, 2, 1, 0]]
        self.assertEqual(sorted(cycles), sorted(expected_cycles), "Should find all Hamiltonian cycles")

    def test_no_hamiltonian_cycle(self):
        """Test a graph with no Hamiltonian cycle."""
        # Define a graph that has no Hamiltonian cycle
        graph = [
            [(0, 0), [1]],          # Node 0 connected to 1
            [(1, 1), [0, 2]],       # Node 1 connected to 0 and 2
            [(2, 2), [1, 3]],       # Node 2 connected to 1 and 3
            [(3, 3), [2]],          # Node 3 connected to 2
        ]
        cycles = permutations.find_hamiltonian_cycles(graph)
        self.assertEqual(cycles, [], "Should find no Hamiltonian cycles")

    def test_disconnected_graph(self):
        """Test a disconnected graph with no Hamiltonian cycle."""
        # Define a disconnected graph
        graph = [
            [(0, 0), [1]],          # Node 0 connected to 1
            [(1, 1), [0]],          # Node 1 connected to 0
            [(2, 2), [3]],          # Node 2 connected to 3
            [(3, 3), [2]],          # Node 3 connected to 2
        ]
        cycles = permutations.find_hamiltonian_cycles(graph)
        self.assertEqual(cycles, [], "Should find no Hamiltonian cycles in a disconnected graph")

    def test_large_graph_no_cycle(self):
        """Test a larger graph where a Hamiltonian cycle is unlikely (e.g., with only a partial connection)."""
        graph = [
            [(0, 0), [1]],             # Node 0 connected to 1
            [(1, 1), [0, 2]],          # Node 1 connected to 0 and 2
            [(2, 2), [1, 3]],          # Node 2 connected to 1 and 3
            [(3, 3), [2, 4]],          # Node 3 connected to 2 and 4
            [(4, 4), [3, 5]],          # Node 4 connected to 3 and 5
            [(5, 5), [4]],             # Node 5 connected to 4
        ]
        cycles = permutations.find_hamiltonian_cycles(graph)
        self.assertEqual(cycles, [], "Should find no Hamiltonian cycles in a partially connected graph")
if __name__ == '__main__':
    unittest.main()
