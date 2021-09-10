# Cian Linehan
# CS2515 Assignment 2
from functools import total_ordering

@total_ordering
class TestClass:
    """ Represents an arbitrary thing, for testing the BST. """

    def __init__(self, field1, field2=None):
        """ Initialise an object. """
        self._field1 = field1
        self._field2 = field2

    def __str__(self):
        """ Return a short string representation of this object. """
        outstr = self._field1
        return outstr

    def full_str(self):
        """ Return a full string representation of this object. """
        outstr = self._field1 + ": "
        outstr = outstr + str(self._field2)
        return outstr

    def __eq__(self, other):
        """ Return True if this object has exactly same field1 as other. """
        if (other._field1 == self._field1):
            return True
        return False

    def __ne__(self, other):
        """ Return False if this object has exactly same field1 as other. """
        return not (self._field1 == other._field1)

    def __lt__(self, other):
        """ Return True if this object is ordered before other.

        A thing is less than another if it's field1 is alphabetically before.
        """
        if other._field1 > self._field1:
            return True
        return False


class BSTNode:
    """ An internal node for a Binary Search Tree.  """

    def __init__(self, item):
        """ Initialise a BSTNode on creation, with value==item. """
        self._element = item
        self._leftchild = None
        self._rightchild = None
        self._parent = None

    def __str__(self):
        """ Return a string representation of the tree rooted at this node.

        The string will be created by an in-order traversal.
        note to self: this orders the elements in the BST increasing from left to right.
        """
        outstr = ''
        node = self
        if node is not None:
            if node._leftchild or node._rightchild is not None:
                if node._leftchild is not None:
                    outstr = outstr + str(node._leftchild.__str__())
                outstr = outstr + str(node._element) + ' '
                if node._rightchild is not None:
                    outstr = outstr + str(node._rightchild.__str__())
                return outstr
            elif node._element is None or node is None:
                return ''
            else:
                return str(node._element) + ' '
        elif node._element is None or node is None:
            return ''

    def _stats(self):
        """ Return the basic stats on the tree. """
        return ('size = ' + str(self.size())
                + '; height = ' + str(self.height()))

    def search(self, searchitem):
        """ Return object matching searchitem, or None.

        Args:
            searchitem: an object of any class stored in the BST

        """
        result = self.search_node(searchitem)
        if result is not None:
            return result._element
        return None

    def search_node(self, searchitem):
        """ Return the BSTNode (with subtree) containing searchitem, or None. 

        Args:
            searchitem: an object of any class stored in the BST
        """

        if searchitem < self._element:
            if self._leftchild is None:
                return None
            return self._leftchild.search_node(searchitem)
        elif searchitem > self._element:
            if self._rightchild is None:
                return None
            return self._rightchild.search_node(searchitem)
        else:
            return self

    def add(self, obj):
        """ Add item to the tree, maintaining BST properties.

        Returns the item added, or None if a matching object was already there.
        :type obj: object
        """
        # pointer to selected node
        current = self
        if obj > current._element:
            if current._rightchild is None:
                newNode = BSTNode(obj)
                newNode._parent = current
                current._rightchild = newNode
                return obj
            else:
                current._rightchild.add(obj)
        elif obj < current._element:
            if current._leftchild is None:
                newNode = BSTNode(obj)
                newNode._parent = current
                current._leftchild = newNode
                return obj
            else:
                current._leftchild.add(obj)
        else:
            pass  # element is already in the BST

    def findmaxnode(self):
        """ Return the BSTNode with maximal element at or below here. """
        if self._rightchild is None:
            return self
        else:
            return self._rightchild.findmaxnode()

    def height(self):
        """ Return the height of this node.

        Note that with the recursive definition of the tree the height of the
        node is the same as the depth of the tree rooted at this node.
        """
        if self is None:
            return 0
        elif self._leftchild is None and self._rightchild is None:
            return 0
        else:
            return 1 + max(BSTNode.height(self._rightchild), BSTNode.height(self._leftchild))

    def size(self):
        """ Return the size of this subtree.

        The size is the number of nodes (or elements) in the tree, 
        including this node.
        """
        if self is None:
            return 0
        elif self._leftchild is None and self._rightchild is None:
            return 1
        else:
            return 1 + BSTNode.size(self._rightchild) + BSTNode.size(self._leftchild)

    def leaf(self):
        """ Return True if this node has no children. """
        if self._rightchild is None and self._leftchild is None:
            return True
        return False

    def semileaf(self):
        """ Return True if this node has exactly one child. """
        if self._leftchild is not None or self._rightchild is not None:
            return True
        return False

    def full(self):
        """ Return true if this node has two children. """
        if self._rightchild is not None and self._leftchild is not None:
            return True
        return False

    def internal(self):
        """ Return True if this node has at least one child. """
        if BSTNode.semileaf(self) or BSTNode.full(self):
            return True
        return False

    def remove(self, searchitem):
        """ Remove and return the object matching searchitem, if there.

        Args:
            searchitem - an object of any class stored in the BST

        Remove the matching object from the tree rooted at this node.
        Maintains the BST properties.
        """
        # node containing this item
        node = self.search_node(searchitem)
        # if the item is in the tree i.e. not None
        if node is not None:
            BSTNode.remove_node(node)
            return searchitem
        return None

    def remove_node(self):
        """ Remove this BSTNode from its tree, and return its element.

        Maintains the BST properties.
        """

        if BSTNode.full(self):
            maxNode = BSTNode.findmaxnode(self._leftchild)
            original = self._element
            self._element = maxNode._element

            if maxNode._parent._rightchild == maxNode:
                maxNode._parent._rightchild = None
            return original

        elif BSTNode.leaf(self):
            element = self._element
            if self._parent is not None:
                if self._parent._rightchild == self:
                    self._parent._rightchild = None
                else:
                    self._parent._leftchild = None
            else:
                self._element = None
            return element

        elif BSTNode.semileaf(self):
            element = self._element
            # special case first - removing semileaf - will replace self elements with that of children
            if self._parent is None:
                if self._rightchild is not None:
                    childOfRemoved = self._rightchild
                    self._rightchild._parent = None
                else:
                    childOfRemoved = self._leftchild
                    self._leftchild._parent = None
                self._element = childOfRemoved._element
                self._rightchild = childOfRemoved._rightchild
                self._leftchild = childOfRemoved._leftchild
                return element

            elif self._rightchild is not None:
                if self._parent._rightchild == self:
                    self._parent._rightchild = self._rightchild
                else:
                    self._parent._leftchild = self._rightchild
                self._rightchild._parent = self._parent
                return element

            else:
                if self._parent._rightchild == self:
                    self._parent._rightchild = self._leftchild
                else:
                    self._parent._leftchild = self._leftchild
                self._leftchild._parent = self._parent
                return element

    def _print_structure(self):
        """ (Private) Print a structured representation of tree at this node. """
        if self._isthisapropertree() == False:
            print("ERROR: this is not a proper Binary Search Tree. ++++++++++")
        outstr = str(self._element) + ' (hgt=' + str(self.height()) + ')['
        if self._leftchild is not None:
            outstr = outstr + "left: " + str(self._leftchild._element)
        else:
            outstr = outstr + 'left: *'
        if self._rightchild is not None:
            outstr = outstr + "; right: " + str(self._rightchild._element) + ']'
        else:
            outstr = outstr + '; right: *]'
        if self._parent is not None:
            outstr = outstr + ' -- parent: ' + str(self._parent._element)
        else:
            outstr = outstr + ' -- parent: *'
        print(outstr)
        if self._leftchild is not None:
            self._leftchild._print_structure()
        if self._rightchild is not None:
            self._rightchild._print_structure()

    def _properBST(self):
        """ Return True if this is the root of a proper BST; False otherwise. 

        First checks that this is a proper tree (i.e. parent and child
        references all link up properly.

        Then checks that it obeys the BST property.
        """
        if not self._isthisapropertree():
            return False
        return self._BSTproperties()[0]

    def _BSTproperties(self):
        """ Return a tuple describing state of this node as root of a BST.

        Returns:
            (boolean, minvalue, maxvalue):
                boolean is True if it is a BST, and false otherwise
                minvalue is the lowest value in this subtree
                maxvalue is the highest value in this subtree
        """
        minvalue = self._element
        maxvalue = self._element
        if self._leftchild is not None:
            leftstate = self._leftchild._BSTproperties()
            if not leftstate[0] or leftstate[2] > self._element:
                return (False, None, None)
            minvalue = leftstate[1]

        if self._rightchild is not None:
            rightstate = self._rightchild._BSTproperties()
            if not rightstate[0] or rightstate[1] < self._element:
                return (False, None, None)
            maxvalue = rightstate[2]

        return (True, minvalue, maxvalue)

    def _isthisapropertree(self):
        """ Return True if this node is a properly implemented tree. """
        ok = True
        if self._leftchild is not None:
            if self._leftchild._parent != self:
                ok = False
            if self._leftchild._isthisapropertree() == False:
                ok = False
        if self._rightchild is not None:
            if self._rightchild._parent != self:
                ok = False
            if self._rightchild._isthisapropertree() == False:
                ok = False
        if self._parent is not None:
            if (self._parent._leftchild != self
                    and self._parent._rightchild != self):
                ok = False
        return ok

    def _testadd():
        node = BSTNode(TestClass("Memento", "11/10/2000"))
        node._print_structure()
        print('> adding Melvin and Howard')
        node.add(TestClass("Melvin and Howard", "19/09/1980"))
        node._print_structure()
        print('> adding a second version of Melvin and Howard')
        node.add(TestClass("Melvin and Howard", "21/03/2007"))
        node._print_structure()
        print('> adding Mellow Mud')
        node.add(TestClass("Mellow Mud", "21/09/2016"))
        node._print_structure()
        print('> adding Melody')
        node.add(TestClass("Melody", "21/03/2007"))
        node._print_structure()
        return node

    def _test():
        node = BSTNode(TestClass("B", "b"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "A")
        node.add(TestClass("A", "a"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "A")
        node.remove(TestClass("A"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(TestClass("C", "c"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "C")
        node.remove(TestClass("C"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "F")
        node.add(TestClass("F", "f"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "B")
        node.remove(TestClass("B")) #big error
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(TestClass("C", "c"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "D")
        node.add(TestClass("D", "d"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(TestClass("C", "c"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "E")
        node.add(TestClass("E", "e"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "B")
        node.remove(TestClass("B")) #big error
        print('Ordered:', node)
        node._print_structure()
        print('removing', "D")
        node.remove(TestClass("D"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "C")
        node.remove(TestClass("C"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "E")
        node.remove(TestClass("E"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "L")
        node.add(TestClass("L", "l"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "H")
        node.add(TestClass("H", "h"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "I")
        node.add(TestClass("I", "i"))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "G")
        node.add(TestClass("G", "g"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "L")
        node.remove(TestClass("L"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "H")
        node.remove(TestClass("H"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "I")
        node.remove(TestClass("I"))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "G")
        node.remove(TestClass("G"))
        print('Ordered:', node)
        node._print_structure()
        print(node)
