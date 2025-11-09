import unittest
from AVLTree import AVLTree, AVLNode


class TestAVLEdgeCounts(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_edge_count_consistency(self):
        """Test that search and insert return same edge count for same path"""
        # Empty tree
        node, search_edges = self.tree.search(5)
        new_node, insert_edges, _ = self.tree.insert(5, "five")
        self.assertEqual(search_edges, insert_edges, "Edge count mismatch for first insertion")

        # Test with more complex scenarios
        values = [(3, "three"), (7, "seven"), (2, "two"), (4, "four")]
        for key, val in values:
            # First search (should fail but give edge count)
            _, search_edges = self.tree.search(key)
            # Then insert
            _, insert_edges, _ = self.tree.insert(key, val)
            self.assertEqual(search_edges, insert_edges,
                             f"Edge count mismatch for key {key}")

    def test_edge_counts_after_rotations(self):
        """Test edge counts when tree structure changes due to rotations"""
        # Create a situation requiring left rotation
        # Insert 10, 20, 30 - should cause rotation
        self.tree.insert(10, "ten")
        _, search_edges_20 = self.tree.search(20)
        _, insert_edges_20, _ = self.tree.insert(20, "twenty")
        self.assertEqual(search_edges_20, insert_edges_20)

        # Search and insert at 30 should give same edge count
        _, search_edges_30 = self.tree.search(30)
        _, insert_edges_30, _ = self.tree.insert(30, "thirty")
        self.assertEqual(search_edges_30, insert_edges_30)

    def test_finger_operations_edge_counts(self):
        """Test edge counts in finger operations"""
        # Build a basic tree
        keys = [50, 30, 70, 20, 40, 60, 80]
        for k in keys:
            self.tree.insert(k, str(k))

        # Test finger search and finger insert consistency
        test_keys = [65, 75, 85,100]  # Keys to test
        for key in test_keys:
            # First finger search
            _, search_edges = self.tree.finger_search(key)
            # Then finger insert
            _, insert_edges, _ = self.tree.finger_insert(key, str(key))
            # _, search_edges = self.tree.finger_search(key)

            self.assertEqual(search_edges, insert_edges,
                             f"Edge count mismatch in finger operations for key {key}")

    def test_edge_cases_edge_counts(self):
        """Test edge counts in various edge cases"""
        # Test with empty tree
        _, edges_empty_search = self.tree.search(1)
        self.assertEqual(edges_empty_search, 0)

        # Insert first node and test
        _, edges_first_insert, _ = self.tree.insert(1, "one")
        self.assertEqual(edges_first_insert, 0)

        # Test searching exact same key after insertion
        _, edges_after_insert = self.tree.search(1)
        self.assertEqual(edges_after_insert, 1)  # Root + 1

        # Create deep path and test all points along it
        values = [10, 8, 6, 4, 2]  # Will create left-heavy tree
        for i, val in enumerate(values):
            # Before insert
            _, search_edges = self.tree.search(val)
            # After insert
            _, insert_edges, _ = self.tree.insert(val, str(val))
            self.assertEqual(search_edges, insert_edges,
                             f"Edge count mismatch at depth {i}")

    def test_boundary_values_edge_counts(self):
        """Test edge counts with boundary value insertions"""
        # Create a balanced tree first
        self.tree.insert(50, "fifty")
        self.tree.insert(25, "twenty-five")
        self.tree.insert(75, "seventy-five")

        # Test minimum possible value
        _, min_search_edges = self.tree.search(-1000000)
        _, min_insert_edges, _ = self.tree.insert(-1000000, "min")
        self.assertEqual(min_search_edges, min_insert_edges)

        # Test maximum possible value
        _, max_search_edges = self.tree.search(1000000)
        _, max_insert_edges, _ = self.tree.insert(1000000, "max")
        self.assertEqual(max_search_edges, max_insert_edges)

    def test_consecutive_values_edge_counts(self):
        """Test edge counts with consecutive value insertions"""
        values = list(range(1, 8))  # 1 to 7

        for val in values:
            # First search (should fail but give edge count)
            _, search_edges = self.tree.search(val)
            # Then insert
            _, insert_edges, _ = self.tree.insert(val, str(val))
            self.assertEqual(search_edges, insert_edges,
                             f"Edge count mismatch for consecutive value {val}")

            # Verify the path length for next value
            if val < 7:
                _, next_edges = self.tree.search(val + 1)
                self.assertTrue(next_edges > 0,
                                f"Invalid edge count for next value after {val}")

    def verify_edge_count(self, key):
        """Helper method to verify edge count matches actual path length"""
        node, edges = self.tree.search(key)
        # Count actual edges by traversing to root
        actual_edges = 0
        if node:
            current = node
            while current.parent:
                actual_edges += 1
                current = current.parent
            actual_edges += 1  # Add 1 as per specification
        self.assertEqual(edges, actual_edges,
                         f"Edge count mismatch for key {key}")


if __name__ == '__main__':
    unittest.main()