import math
import unittest
from unittest.mock import patch

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
        # Mock graph with (x, y) coordinates and neighbor indices
        [(0, 0), [1]],  # Node (0,0) with neighbor [1]
        [(200, -200), [0, 2]],  # Node (200,-200) with neighbors [0, 2]
        [(200, -400), [1]]  # Node (200,-400) with neighbor [1]
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


if __name__ == '__main__':
    unittest.main()
