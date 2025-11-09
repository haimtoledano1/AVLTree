# AVLTree

A clean and efficient Python implementation of an AVL (self-balancing binary search) tree with insert, delete, search, and traversal operations.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Performance](#performance)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview
This repository contains an implementation of an AVL tree in Python. AVL trees are height-balanced binary search trees that guarantee O(log n) time complexity for insertion, deletion, and lookup operations by maintaining a balance factor and performing rotations when needed.

## Features
- Insert, delete, and search operations
- In-order, pre-order, and post-order traversals
- Height and balance-factor calculations
- Self-balancing via single and double rotations
- Clear and well-documented Python API suitable for learning and small projects

## Installation
Clone the repository:

```bash
git clone https://github.com/haimtoledano1/AVLTree.git
cd AVLTree
```

If this project is packaged as a module (not included here), install via pip:

```bash
pip install avltree
```

## Usage
Below is an example of how you might use the AVL tree implementation. Adjust import paths to match the actual module structure in this repository.

```python
from avltree import AVLTree

# Create a tree and insert values
tree = AVLTree()
for value in [10, 20, 5, 6, 15]:
    tree.insert(value)

# Search
print(tree.search(15))  # True
print(tree.search(99))  # False

# Traversals
print(tree.in_order_traversal())   # [5, 6, 10, 15, 20]
print(tree.pre_order_traversal())  # depends on rotations

# Delete
tree.delete(10)
print(tree.in_order_traversal())
```

## API
Typical methods (names may vary depending on the implementation in this repo):
- insert(value)
- delete(value)
- search(value) -> bool
- in_order_traversal() -> list
- pre_order_traversal() -> list
- post_order_traversal() -> list
- height() -> int

Check the source files to confirm exact class and method names.

## Performance
- Average and worst-case time complexity for insert/delete/search: O(log n)
- Space complexity: O(n)

## Testing
If tests are included, run them with pytest:

```bash
pytest
```

## Contributing
Contributions are welcome. Please open issues or pull requests with a clear description of changes. Add tests for new behavior and adhere to PEP 8.

## License
No license specified. If you want to open-source this project, add a LICENSE file (e.g., MIT, Apache-2.0).

## Author
haimtoledano1