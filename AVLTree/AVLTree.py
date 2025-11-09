"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value, left=None, right=None, parent=None):
		self.key = key
		self.value = value
		self.left = left
		self.right = right
		self.parent = parent
		self.height = 0 if key is not None else -1
		#just for testing
		# self._size = 0


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None

# Define the external leaf as singleton object (all external will point to this)
EXTERNAL_LEAF = AVLNode(key=None, value=None)


"""
A class implementing an AVL tree.
"""
class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self._size = 0  # Number of real nodes in the tree
		self.max = self.root # pointer to maximum node

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		x , e, _ = _search_from(self.root, key)
		return x, e


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node- the maximum of tree and ending node+1.
	"""
	def finger_search(self, key):
		if self.max is None:
			return None, 0
		ancestor , edges_up = self._finger_track_up(key)
		# go down until key is found
		node , edges_down, _ = _search_from(ancestor, key)
		edges = edges_down + edges_up
		return node, edges


	# helper that finds first common ancestor of max and key and  used in finger_search and finger_insert
	def _finger_track_up(self, key):
		curr = self.max_node()
		edges = 0
		# go up until key is in subtree of current node
		while curr.parent is not None and (curr.parent.key >= key):
			curr = curr.parent
			edges += 1
		return curr, edges

	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		_ ,edges, parent = _search_from(self.root, key)
		new_node , promotes = self._insert_to_parent(parent, key, val)
		return new_node, edges, promotes

	#helper function to insert a new node to the parent and handle all logic and rebalancing. used in insert and insert_finger
	def _insert_to_parent(self, parent, key, val):
		if parent is None:
			self.root = AVLNode(key, val, parent=None, left=EXTERNAL_LEAF, right=EXTERNAL_LEAF)
			self._size += 1
			self.max = self.root
			return self.root, 0
		new_node = AVLNode(key, val, parent=parent, left=EXTERNAL_LEAF, right=EXTERNAL_LEAF)
		if key > parent.key:
			parent.right = new_node
		else:
			parent.left = new_node
		self._size += 1
		# update max if needed
		if self.max is not None and key > self.max.key:
			self.max = new_node

		# case A: parent is not a leaf - valid AVL tree
		if parent.height == 1:
			return new_node, 0
		# case B: parent is a leaf
		promotes = 0

		curr = new_node
		# case 1 - promote
		while curr.parent  and curr.height >= curr.parent.height:
			bf = _balance_factor(curr.parent)
			# notice bf ==0 is impossible here.
			if bf in [-1, 1]:  # case 1 - only promote
				_update_height(curr.parent)
				promotes += 1
				curr = curr.parent
			else:
				curr = _rebalance(curr.parent)
				break # we break since we know in this case we finish


		# check if root has changed due to rotations. in any rotation on the root it drops maximum by 1
		if self.root.parent is not None:
			self.root = self.root.parent

		return new_node, promotes

	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		if self.max is None:
			self.root = AVLNode(key, val, parent=None, left=EXTERNAL_LEAF, right=EXTERNAL_LEAF)
			self._size += 1
			self.max = self.root
			return self.root, 0, 0
		ancestor,edges_up =  self._finger_track_up(key)
		_, edges_down, parent = _search_from(ancestor, key)
		edges = edges_down + edges_up
		new_node, promotes = self._insert_to_parent(parent, key, val)
		return new_node, edges, promotes

	"""deletes node from the dictionary
	
	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		# Case 1: Node has two children, we swap values with the predecessor (must be leaf) and delete the predecessor
		if node.left.is_real_node() and node.right.is_real_node():
			pred = _predecessor(node)
			node.key, pred.key = pred.key, node.key
			node.value, pred.value = pred.value, node.value
			node = pred # node to be deleted

		# logic for deleting a leaf node. for case 1 and 2- if node was originally leaf
		if not node.left.is_real_node() and not node.right.is_real_node():
			if node.parent is None: # if node is root and also leaf
				self.root = None
				self._size = 0
				self.max = None
				return
			else:
				if node.parent.left == node:
					node.parent.left = EXTERNAL_LEAF
				else:
					node.parent.right = EXTERNAL_LEAF

		#case 3: node has exactly one child
		elif node.left.is_real_node() or node.right.is_real_node():
			child = node.left if node.left.is_real_node() else node.right
			child.parent = node.parent
			if node.parent:
				if node.parent.left == node:
					node.parent.left = child
				else:
					node.parent.right = child
			else: # we deleted the root
				self.root = child
		# now we start rebalancing from parent to root
		curr = node.parent
		while curr:
			_update_height(curr)
			if abs(_balance_factor(curr)) > 1:
				curr = _rebalance(curr)
			curr = curr.parent

		# final updates
		# check if root has changed due to rotations. in any rotation on the root it drops maximum by 1
		if self.root.parent is not None:
			self.root = self.root.parent
		self._size -= 1
		# update max if needed
		if self.max.key == node.key:
			self.max = _find_max(self.root)
		return


	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""

	def join(self, tree2, key, val):

		if tree2.root is None or not tree2.root.is_real_node():
			self.insert(key, val)
			return
		if self.root is None or not self.root.is_real_node():
			self.root = tree2.root
			self.max = tree2.max
			self._size = tree2._size
			self.insert(key, val)
			return

		# determine which tree is of greater keys
		right_tree = self if self.root.key > key else tree2
		left_tree = self if self.root.key < key else tree2

		if left_tree.root.height > right_tree.root.height + 1:
			return self._join_with_bigger_subtree(
				bigger_tree=left_tree,
				smaller_tree=right_tree,
				key=key,
				val=val,
				is_left_bigger=True
			)
		if right_tree.root.height > left_tree.root.height + 1:
			return self._join_with_bigger_subtree(
				bigger_tree=right_tree,
				smaller_tree=left_tree,
				key=key,
				val=val,
				is_left_bigger=False
			)

		# if trees differ by at most 1 in height
		new_root = AVLNode(key, val, left=left_tree.root, right=right_tree.root)
		left_tree.root.parent = new_root
		right_tree.root.parent = new_root
		_update_height(new_root)
		self.root = new_root
		self._size += tree2._size + 1
		self.max = right_tree.max
		return

	def _join_with_bigger_subtree(self, bigger_tree, smaller_tree, key, val, is_left_bigger):
		"""Helper method to join trees when one subtree is significantly bigger"""
		# go down in bigger until we find a node with height of smaller.root.height
		curr = bigger_tree.root
		external_stop_flag = False
		while curr.height > smaller_tree.root.height:
			if (is_left_bigger and not curr.right.is_real_node()) or (not is_left_bigger and not curr.left.is_real_node()):
				external_stop_flag = True
				break
			else:
				curr = curr.right if is_left_bigger else curr.left


		# connect and cut what's needed
		if is_left_bigger:
			if external_stop_flag:
				x_node = AVLNode(key, val, parent=curr, left=EXTERNAL_LEAF, right=smaller_tree.root)
				curr.right = x_node
			else:
				x_node = AVLNode(key, val, parent=curr.parent, left=curr, right=smaller_tree.root)
				curr.parent.right = x_node
				curr.parent = x_node
		else:
			if external_stop_flag:
				x_node = AVLNode(key, val, parent=curr, left=smaller_tree.root, right=EXTERNAL_LEAF)
				curr.left = x_node
			else:
				x_node = AVLNode(key, val, parent=curr.parent, left=smaller_tree.root, right=curr)
				curr.parent.left = x_node
				curr.parent = x_node

		smaller_tree.root.parent = x_node
		_update_height(x_node)

		# rebalance from x_node to root
		curr = x_node
		# rebalancing logic
		while curr.parent is not None and  curr.height >= curr.parent.height :
			bf = _balance_factor(curr.parent)
			# notice bf ==0 is impossible here.
			if bf in [-1, 1]:  # case 1 - only promote
				_update_height(curr.parent)
				curr = curr.parent
			else: # case 2 - rotate
				curr = _rebalance(curr.parent)

		# check if root has changed due to rotations. in any rotation on the root it drops maximum by 1
		if bigger_tree.root.parent is not None:
			bigger_tree.root = bigger_tree.root.parent

		self.max = smaller_tree.max if is_left_bigger else bigger_tree.max
		self.root = bigger_tree.root
		self._size = bigger_tree._size + smaller_tree._size + 1
		return

	"""splits the dictionary at a given node
	be aware after this function is called the size property of the dictionary is not valid anymore

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		# Initialize the subtrees based on the given node
		larger_than_node = AVLTree() # Subtree with nodes larger than the current node's key
		smaller_than_node = AVLTree() # Subtree with nodes smaller than the current node's key
		if node is None or not node.is_real_node():
			return smaller_than_node, larger_than_node
		if node.left.is_real_node():
			smaller_than_node.root = node.left
			node.left.parent = None
		if node.right.is_real_node():
			larger_than_node.root = node.right
			node.right.parent = None

		# Traverse upwards from the given node to update the subtrees structure
		curr_parent = node.parent
		curr_child = node
		while curr_parent :
			temp_tree = AVLTree()
			if curr_child == curr_parent.right:# If the current node is in the right subtree of its parent
				if curr_parent.left.is_real_node():
					temp_tree.root = curr_parent.left
					curr_parent.left.parent = None
				# Join the parent's left subtree with the smaller subtree
				smaller_than_node.join(temp_tree, curr_parent.key, curr_parent.value)
			else: # If the current node is in the left subtree of its parent
				if curr_parent.right.is_real_node():
					temp_tree.root = curr_parent.right
					curr_parent.right.parent = None
				# Join the parent's right subtree with the larger subtree
				larger_than_node.join(temp_tree, curr_parent.key, curr_parent.value)
			# Move up to the parent node for the next iteration
			curr_child = curr_parent
			curr_parent = curr_parent.parent
		smaller_than_node.max = _find_max(smaller_than_node.root)
		larger_than_node.max = _find_max(larger_than_node.root)
		# Return the two resulting subtrees
		return smaller_than_node, larger_than_node

	"""returns an s array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		result = []
		def inorder_traversal(node):
			if not node or not node.is_real_node():
				return
			inorder_traversal(node.left)
			result.append((node.key, node.value))
			inorder_traversal(node.right)

		inorder_traversal(self.root)
		return result

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self._size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root




# independent helper functions

# returns the maximum node in the tree iterating in the right extreme of the tree. used in split and predecessor
def _find_max(node):
	if node is None or not node.is_real_node():
		return None
	curr = node
	while curr.right.is_real_node():
		curr = curr.right
	return curr
# stand-alone helper functions
# calculates the balance factor of the node
def _balance_factor(node):
	if not node or not node.is_real_node():
		return 0
	return node.left.height - node.right.height

# calculates the height of the node based on its children
def _update_height(node):
	if not node or not node.is_real_node():
		return
	node.height = 1 + max(node.left.height, node.right.height)


#cheks what rotation is needed (should handle all cases possible) and calls the appropriate function finally returns the new root of the subtree
def _rebalance(node):
	bf = _balance_factor(node)
	if bf > 1: # left heavy
		if _balance_factor(node.left) >=0: # left left heavy
			return _rotate_right(node)
		else: # left right heavy
			_rotate_left(node.left)
			return _rotate_right(node)
	elif bf < -1:# right heavy
		if _balance_factor(node.right) <= 0: # right right heavy
			return _rotate_left(node)
		else: # right left heavy
			_rotate_right(node.right)
			return _rotate_left(node)
	return node

# rotates and returns the new root of the subtree, must ensure all is connected properly
def _rotate_left(z):
	#     z                              y
	#    /  \                           / \
	#   T1   y         Left Rotate     z   X
	#       / \       ============>   / \
	#      T2  X                    T1  T2
	y = z.right
	parent = z.parent

	t2 = y.left
	z.right = t2
	t2.parent = z
	_update_height(z)

	y.left = z
	z.parent = y
	_update_height(y)

	y.parent = parent

	# update parent
	if parent is None:
		return y
	elif parent.left == z:
		parent.left = y
	else:
		parent.right = y
	return y

# rotates and returns the new root of the subtree, must ensure all is connected properly
def _rotate_right(z):
	#       z                             y
	#      / \                           / \
	#     y   T3        Right Rotate    X   z
	#    / \           ============>       / \
	#   X   T2                           T2   T3
	y = z.left
	parent = z.parent

	t2 = y.right
	z.left = t2
	t2.parent = z
	_update_height(z)

	y.right = z
	z.parent = y
	_update_height(y)

	y.parent = parent

	# update parent
	if parent is None:
		return y
	elif parent.left == z:
		parent.left = y
	else:
		parent.right = y
	return y

# @returns: a 3-tuple (node,edges,parent) where node is the searched node or none if not found,
# edges is the number of edges on the path between the starting node and new node ,
# parent is the parent of the searched node. used in insert, and insert finger
def _search_from(node, key):
	if node is None or not node.is_real_node():
		return None, 0, None
	curr = node
	edges = 0
	parent = node
	while curr.is_real_node():
		if curr.key == key:
			return curr , edges+1, curr.parent
		elif curr.key < key:
			parent = curr
			curr = curr.right
		else:
			parent = curr
			curr = curr.left
		edges += 1
	return None, edges, parent

# returns the predecessor of the node
def _predecessor(node):
	if not node or not node.is_real_node():
		return None

	# Case 1: Node has a left subtree
	if node.left.is_real_node():
		return _find_max(node.left)

	# Case 2: No left subtree - go up to the first parent for which node is in the right subtree
	curr = node
	parent = curr.parent
	while parent and parent.left == curr:
		curr = parent
		parent = parent.parent
	return parent