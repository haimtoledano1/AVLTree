# AVL Tree (Python Implementation)

## Description

This project is a Python implementation of an AVL tree, a self-balancing binary search tree. It is intended for educational purposes to demonstrate the concepts and implementation of an AVL tree.

## Main Features

*   **Insert:** Add new nodes to the tree while maintaining the AVL property.
*   **Delete:** Remove nodes from the tree and rebalance it.
*   **Search:** Find nodes with a specific key.
*   **Join:** Merge two AVL trees.
*   **Split:** Divide a tree into two smaller trees.
*   **Traversals:** Convert the tree to a sorted array.

## File Structure

```
AVLTree/
├───tests/
│   ├───avl-test-suite.py
│   ├───TestAVLTree.py
│   └───tester.py
├───AVLTree Function Documentation.pdf
├───AVLTree.py
├───experiment1.py
└───proj1_2024a.pdf
```

## Usage

```python
from AVLTree import AVLTree

# Create a new AVL Tree
tree = AVLTree()

# Insert some values
tree.insert(10, "value10")
tree.insert(5, "value5")
tree.insert(15, "value15")

# Search for a value
node, edges = tree.search(5)
if node:
    print(f"Found node with key 5 and value {node.value}")

# Delete a value
node_to_delete, _ = tree.search(10)
if node_to_delete:
    tree.delete(node_to_delete)

# Print the tree as an array
print(tree.avl_to_array())
```

## Testing

To run the tests, navigate to the project's root directory and run the following command:

```bash
python AVLTree/tests/TestAVLTree.py
```

### Randomized Tester

The project also includes a randomized tester (`tester.py`) that performs a series of random operations (insert, delete, split, join) on the AVL tree and validates the tree's properties after each step.

To run the randomized tester:

```bash
python AVLTree/tests/tester.py
```
You can tweak the tester's behavior by editing constants at the top of
`tests/tester.py`, such as:

* `NUM_OF_TESTS` – number of test runs to execute.
* `NUM_OF_STEPS` – random operations per run.
* `MIN_KEY`/`MAX_KEY` – range of keys generated.
* `step_weights` – relative probability of each operation.
* `BULK_MODE` – continue running even if a failure occurs.


The tester will save the results, including any failures, to a file named `avl_tester_results.json` in your home directory.

## Dependencies

The core `AVLTree.py` implementation has no external dependencies.

However, some of the other scripts have dependencies:
* The randomized tester (`AVLTree/tests/tester.py`) uses the `tqdm` library to display progress bars.
* The experiment script (`AVLTree/experiment1.py`) uses the `pandas` library for data analysis.

You can install these dependencies using pip:

```bash
pip install tqdm pandas
```

## License

This project is for educational purposes. You are free to use and modify the code.