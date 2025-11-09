import unittest
from AVLTree import AVLTree, AVLNode

class TestAVLTree(unittest.TestCase):

    def setUp(self):
        self.tree = AVLTree()

    def test_empty_tree(self):
        self.assertIsNone(self.tree.get_root())
        self.assertEqual(self.tree._size, 0)

    def test_insert_single_node(self):
        node, edges, promotes = self.tree.insert(10, "A")
        self.assertEqual(node.key, 10)
        self.assertEqual(node.value, "A")
        self.assertEqual(self.tree.get_root().key, 10)
        self.assertEqual(self.tree._size, 1)
        self.assertEqual(edges, 0)
        self.assertEqual(promotes, 0)

    def test_insert_multiple_nodes(self):
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(5, "C")
        self.tree.insert(15, "D")
        self.assertEqual(self.tree._size, 4)
        self.assertEqual(self.tree.get_root().key, 10)
        self.assertEqual(self.tree.max_node().key, 20)

    def test_search_existing_key(self):
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        node, edges = self.tree.search(20)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 20)
        self.assertEqual(node.value, "B")
        self.assertEqual(edges, 2)

    def test_search_non_existing_key(self):
        self.tree.insert(10, "A")
        node, edges = self.tree.search(30)
        self.assertIsNone(node)
        self.assertEqual(edges, 1)

    def test_delete_leaf_node(self):
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        node, _, _ = self.tree.insert(5, "C")
        self.tree.delete(node)
        self.assertEqual(self.tree._size, 2)
        self.assertIsNone(self.tree.search(5)[0])

    def test_delete_internal_node(self):
        self.tree.insert(10, "A")
        node, _, _ = self.tree.insert(20, "B")
        self.tree.insert(15, "C")
        self.tree.delete(node)
        self.assertEqual(self.tree._size, 2)
        self.assertIsNone(self.tree.search(20)[0])

    def test_join_trees(self):
        tree1 = AVLTree()
        tree2 = AVLTree()
        tree1.insert(10, "A")
        tree1.insert(5, "B")
        tree2.insert(20, "C")
        tree2.insert(25, "D")
        tree1.join(tree2, 15, "E")
        self.assertEqual(tree1._size, 5)
        self.assertEqual(tree1.max_node().key, 25)
        self.assertEqual(tree1.get_root().key, 15)

    def test_split_tree(self):
        self.tree.insert(10, "A")
        node, _, _ = self.tree.insert(20, "B")
        self.tree.insert(5, "C")
        left_tree, right_tree = self.tree.split(node)
        # self.assertEqual(left_tree.size, 2)
        # self.assertEqual(right_tree.size, 0)
        self.assertEqual(left_tree.max_node().key, 10)

    def test_avl_to_array(self):
        self.tree.insert(10, "A")
        self.tree.insert(20, "B")
        self.tree.insert(5, "C")
        self.assertEqual(self.tree.avl_to_array(), [(5, "C"), (10, "A"), (20, "B")])

    def test_balancing(self):
        self.tree.insert(30, "A")
        self.tree.insert(20, "B")
        self.tree.insert(10, "C")
        self.assertEqual(self.tree.get_root().key, 20)

if __name__ == '__main__':
    unittest.main()
