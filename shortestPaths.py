# Cian Linehan 119301381
# CS2516 Shortest Paths CA

# ----------------------------------------------------------------------------------------------------------------------
# Start of Adaptable Priority Queue ADT
# ----------------------------------------------------------------------------------------------------------------------

import time

class BinaryHeap:
    """
    Class for Binary Heap ADT as an array based heap for use in AdaptablePQ.
    """
    def __init__(self):
        self._array = []

    def left(self, element):
        i = element.index
        index = (2*i) + 1
        if index < self.length():
            return self._array[index]

    def right(self, element):
        i = element.index
        index = (2*i) + 2
        if index < self.length():
            return self._array[index]

    def parent(self, element):
        i = element.index
        index = (i-1) // 2
        if 0 <= index < self.length():
            return self._array[index]

    def add(self, element):
        self._array.append(element)
        element.index = self.length() - 1
        # heapify, only looking at parent
        self.heapify(element, lookAtChildrenOnly=False)

    def min(self):
        return self._array[0]

    def remove_min(self):
        if self.is_empty():
            return None

        elif self.length() > 1:
            self._array[0], self._array[-1] = self._array[-1], self._array[0]
            toRemove = self._array[-1]
            self._array[0].index = 0
            del self._array[-1]
            # heapify, only looking at the childre
            self.heapify(self._array[0], lookAtChildrenOnly=True)
        # only one element in the heap, no need for swapping
        else:
            toRemove = self._array[0]
            del self._array[0]
        return toRemove

    def length(self):
        return len(self._array)

    def is_empty(self):
        return len(self._array) == 0

    def heapify(self, element, lookAtChildrenOnly=False):
        """
        Function to reorganise heap focusing on one element, only looking up or down the heap.
        """
        left = self.left(element)
        right = self.right(element)
        if self.length() > 1:
            # if new key is bigger then only need to try bubble down, otherwise only need to try bubble up
            if lookAtChildrenOnly:
                if left is None and right is not None:
                    smallest = right
                elif left is not None and right is None:
                    smallest = left
                elif left is None and right is None:
                    # no children, so stop
                    return
                else:
                    smallest = min(left, right)
                if element > smallest:
                    # swap with smallest child
                    self._array[element.index], self._array[smallest.index] =\
                        self._array[smallest.index], self._array[element.index]
                    # swap indices of elements
                    element.index, smallest.index = smallest.index, element.index
                    self.heapify(element, lookAtChildrenOnly=True)

            else:
                parent = self.parent(element)
                if parent is None:
                    return
                elif parent is not None:
                    if element < parent:
                        # swap with parent
                        self._array[element.index], self._array[parent.index] =\
                            self._array[parent.index], self._array[element.index]
                        # swap indices of elements
                        element.index, parent.index = parent.index, element.index
                        self.heapify(element)


class Element:
    """
    Class for element object for use in Adaptable Priority Queue.

    Key as priority, value as vertex label.
    """
    def __init__(self, key, value, index=None):
        self._key = key
        self._value = value
        self._index = index

    def __eq__(self, other):
        return self._key == other.key

    def __lt__(self, other):
        return self._key < other.key

    def __gt__(self, other):
        return self._key > other.key

    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new):
        self._index = new

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new):
        self._key = new

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        self._value = new


class AdaptablePQ:
    """
    Class for Adaptable Priority Queue ADT using dictionary lookup table and binary heap.
    """
    def __init__(self):
        # lookup has vertex label as key and element object as value
        self._lookup = {}
        self._heap = BinaryHeap()

    def add(self, cost, vertex):
        if vertex not in self._lookup.keys():
            element = Element(cost, vertex)
            self._heap.add(element)
            self._lookup[vertex] = element

    def updateCost(self, vertex, newCost):
        element = self._lookup[vertex]
        oldCost = element.key

        element.key = newCost
        if newCost > oldCost:
            self._heap.heapify(element, lookAtChildrenOnly=True)
        else:
            self._heap.heapify(element, lookAtChildrenOnly=False)

    def remove_min(self):
        element = self._heap.remove_min()
        return element

    def min(self):
        return self._heap.min()

    def is_empty(self):
        return self._heap.is_empty()

    def get_priority(self, vertex):
        return self._lookup[vertex].key

    def presenceOfV(self, vertex):
        if vertex in self._lookup.keys():
            return True
        return False
# ----------------------------------------------------------------------------------------------------------------------
# End of Adaptable Priority Queue ADT
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Start of Graph ADT - part (i)
# ----------------------------------------------------------------------------------------------------------------------
""" From sample solutions for first lab on graphs.

    Implements the graph as a map of (vertex,edge-map) pairs.
"""

class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element


class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element=1):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
            v - start vertex
            w - end vertex
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, x):
        self._element = x

class Graph:
    """ Represent a simple graph.

    This version maintains directed or undirected (default) graphs, and assumes no
    self loops.

    Implements the Adjacency Map style. Also maintains a top level
    dictionary of vertices.
    """

    # Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.

    def __init__(self, directed=False):
        """ Create an initial empty graph. """
        self._verticesMap = dict()
        self.__directed = directed

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._verticesMap:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    # -----------------------------------------------------------------------#
    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._verticesMap)

    def num_edges(self):
        """ Return the number of edges in the graph.

        """
        num = 0
        for v in self._verticesMap:
            num += len(self._verticesMap[v])  # the dict of edges for v
        if not self.__directed:
            return num // 2     # divide by 2, since each edge appears in the
                                # vertex list for both of its vertices
        else:
            return num  # since each edge in a directed graph is not repeated unless

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._verticesMap]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._verticesMap:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._verticesMap:
            for w in self._verticesMap[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._verticesMap[v][w].start() == v:
                    edgelist.append(self._verticesMap[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident from v.

        Args:
            v - a vertex object
        """
        if v in self._verticesMap:
            edgelist = []
            for w in self._verticesMap[v]:
                edgelist.append(self._verticesMap[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

            If one way, then v is start vertex and w end.
        Args:
            v - a vertex object
            w - a vertex object

        """
        if (self._verticesMap is not None
                and v in self._verticesMap
                and w in self._verticesMap[v]):
            return self._verticesMap[v][w]
        return None

    def out_degree(self, v):
        """ Return the out-degree for vertex v

            Use for directed graphs only
        :param v: vertexADT objecte
        :return: out-degree
        """
        if self.__directed:
            count = 0
            for _ in self._verticesMap[v]:
                count += 1
            return count

    def in_degree(self, v):
        """ Return the in-degree for vertex v

            Use for directed graphs only
        :param v: vertexADT object
        :return: out-degree
        """
        if self.__directed:
            count = 0
            for vertex in self._verticesMap.keys():
                for end in self._verticesMap[vertex]:
                    if end is v:
                        count += 1
            return count

    def degree(self, v):
        """ Return the degree of vertex v.

            Use for undirected graphs only.
        Args:
            v - a vertex object
        """
        if not self.__directed:
            return len(self._verticesMap[v])

    # ----------------------------------------------------------------------#
    # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._verticesMap[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._verticesMap:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element, oneWay=False):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        If the edge is one way, then will only add to the map of v.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._verticesMap or w not in self._verticesMap:
            return None
        e = Edge(v, w, element)
        self._verticesMap[v][w] = e
        # Only add edge to w map if the graph is not directed
        if not oneWay:
            self._verticesMap[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    # ---------------------------------------------------------------------#
    # Additional methods to explore the graph

    def highestdegreevertex(self):
        """ Return the vertex with highest degree.

            Use for undirected graphs only.
        """
        if not self.__directed:
            hd = -1
            hdv = None
            for v in self._verticesMap:
                if self.degree(v) > hd:
                    hd = self.degree(v)
                    hdv = v
            return hdv

    # ---------------------------------------------------------------------#
    # Methods for interacting with Dijkstra's Algorithm

    def runDijkstra(self, v, printResults=False, label=False):
        """
        Run Dijkstra's Algorithm on graph starting from Vertex object v
        Currently only handles undirected, unweighted graphs.

        :param v: source vertex to begin Djikstra's algorithm from
        :param printResults: if True then print the results in the form; Vertex, Cost and predecessor.
        :param label: if True, then function will assume you have entered
        start vertex by label not vertex object.
        :rtype: dict where the vertex is a key, and its value is
        a pair consisting of the path length from the source and the preceding
        vertex.
        """
        openAPQ = AdaptablePQ()
        predsDict = {}
        closedDict = {}
        if label:
            v = self.get_vertex_by_label(v)

        # 1st loop from source
        cost, vertexADT, vertexLabel = 0.0, v, v.element()
        neighbours = list(self._verticesMap[vertexADT].keys())
        predsDict[vertexADT] = None
        for neighbour in neighbours:
            if neighbour != vertexADT:
                newCost = float(self._verticesMap[vertexADT][neighbour].element) + float(cost)
                openAPQ.add(newCost, neighbour)
                predsDict[neighbour] = vertexADT
        predecessor = predsDict[vertexADT]
        del predsDict[vertexADT]
        closedDict[vertexADT] = (cost, predecessor)

        # loop over all other elements in the connected component of v
        while not openAPQ.is_empty():
            v = openAPQ.remove_min()
            if v.key not in closedDict.keys():
                cost, vertexADT, vertexLabel = v.key, v.value, v.value.element()
                neighbours = self._verticesMap[vertexADT].keys()
                for neighbour in neighbours:
                    if neighbour not in closedDict.keys():
                        newCost = float(self._verticesMap[vertexADT][neighbour].element) + float(cost)
                        if not openAPQ.presenceOfV(neighbour):
                            openAPQ.add(newCost, neighbour)
                            predsDict[neighbour] = vertexADT
                        elif newCost < openAPQ.get_priority(neighbour):
                            openAPQ.updateCost(neighbour, newCost)
                            predsDict[neighbour] = vertexADT
                predecessor = predsDict[vertexADT]
                del predsDict[vertexADT]
                closedDict[vertexADT] = (cost, predecessor)

        if printResults:
            for vertex in closedDict.keys():
                print("Vertex: " + str(vertex.element()) + "\tCost: " + str(closedDict[vertex][0])
                      + "\tPredecessor: " + str(closedDict[vertex][1]))
        return closedDict

    # custom function for my own testing, also contains some shortest path material. This is not the function
    # specified in the assignment. See RouteMap class for said function.
    def _getShortestPath(self, start, end, printResults=False, label=False):
        """
        Use Dijkstra's Algorithm to compute the shortest path.
        Optional parameters to help with testing.

        :param start: start vertexADT
        :param end: end vertexADT (goal)
        :param printResults: if True, then will also print results in a readable format
        :param label: if True, then function will assume you have entered
        start and end vertices by label not vertex object.
        :return: A list, 1st element - Cost to end vertex from start
                         2nd element - Predecessor VertexADT of end vertex
                         3rd element - A list which contains a tuple of form (cost, predecessor VertexADT)
        """
        if label:
            start = self.get_vertex_by_label(start)
            end = self.get_vertex_by_label(end)

        closedDict = self.runDijkstra(start)
        pathStr = str(end.element())
        pathList = [closedDict[end][0], closedDict[end][1], []]
        predecessor = closedDict[end][1]
        while predecessor is not None:
            pathStr = str(predecessor.element()) + "-" + pathStr
            pathList[2].append((closedDict[predecessor][0], predecessor))
            predecessor = closedDict[predecessor][1]
        pathStr = "Path: " + pathStr

        pathList[2].reverse()
        if printResults:
            print("Vertex: " + str(end.element()) + "\tCost: " + str(closedDict[end][0])
                  + "\tPredecessor: " + str(closedDict[end][1]))
            print(pathStr)
        return pathList

    @staticmethod
    def graphReaderFormatOne(filename):
        """ Read and return the route map in filename.

            For use in graphs of format one - simple graph
        """
        graph = Graph()
        file = open(filename, 'r')

        entry = file.readline()
        # either 'Node' or 'Edge'
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            vertex = graph.add_vertex(nodeid)
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'vertices and added into the graph')
        num = 0
        while entry == 'Edge\n':
            num += 1
            source = int(file.readline().split()[1])
            sv = graph.get_vertex_by_label(source)
            target = int(file.readline().split()[1])
            tv = graph.get_vertex_by_label(target)
            length = float(file.readline().split()[1])
            edge = graph.add_edge(sv, tv, length)
            file.readline()  # read the one-way data
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'edges and added into the graph')
        print(graph)
        return graph

# ----------------------------------------------------------------------------------------------------------------------
# End of Graph ADT - part (i)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Start of Graph ADT - part (ii) for use in roadmaps
# ----------------------------------------------------------------------------------------------------------------------

class RouteMap(Graph):

    def __init__(self):
        super().__init__()
        self._coords = {}
        self._vertexRefs = {}

    def __str__(self):
        if self.num_edges() < 100 and self.num_vertices() < 100:
            tupl = Graph.__str__(self)
            # return amount of edges and vertices only, don't print them all
            return tupl[0]
        return "Graph too large to fully print"

    def add_vertex(self, element, coord1, coord2):
        v = Graph.add_vertex(self, element)
        self._coords[v] = (coord1, coord2)
        self._vertexRefs[element] = v

    def get_vertex_by_label(self, element):
        try:
            return self._vertexRefs[element]
        except Exception as e:
            print(str(e) + "\nVertex not found in reference dictionary.")
            return e

    @staticmethod
    def graphReaderCorkCity(filename):
        """ Read and return the route map in filename.

            For use in graphs of Road Map format
        """
        graph = RouteMap()
        file = open(filename, 'r')

        entry = file.readline()
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            gps_coords = file.readline().split() # read in gps coords
            gps1 = gps_coords[1]
            gps2 = gps_coords[2]
            vertex = graph.add_vertex(nodeid, gps1, gps2)
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'vertices and added into the graph')
        num = 0
        while entry == 'Edge\n':
            num += 1
            source = int(file.readline().split()[1])
            sv = graph.get_vertex_by_label(source)
            target = int(file.readline().split()[1])
            tv = graph.get_vertex_by_label(target)
            file.readline() # discard length data for now - only interested in average time
            time = float(file.readline().split()[1])
            edge = graph.add_edge(sv, tv, time)
            file.readline()  # read the one-way data
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'edges and added into the graph')
        print(graph)
        return graph

    # assuming v and w are the labels not VertexADT?
    def sp(self, v, w, label=True, printPath=False):
        """Get shortest path from v to w

        :return: list of vertices in the shortest path from v to w, also containing
         the cost from v to that vertex.
        """
        if label:
            v = self.get_vertex_by_label(v)
            w = self.get_vertex_by_label(w)
        splist = self._getShortestPath(v, w)[2]

        if printPath:
            self.printShortestPath(splist)
        return splist

    def printShortestPath(self, splist):

        print("{}\t{}\t{}\t{}\t\t{}".format("type", "latitude", "longitude", "element", "cost"))
        for tuple in splist:
            cost = str(tuple[0])
            vertex = tuple[1]
            element = str(vertex.element())
            lat, long = str(self._coords[vertex][0]), str(self._coords[vertex][1])

            # add in whitespace for shorter element numbers
            if len(element) < 10:
                i = 10 - len(element)
                i *= " "
                element = element + i
            print("{}\t     {}\t{}\t{}\t{}".format("W", lat, long, element, cost))
            # print("W\t" + str(lat) + "\t" + str(long) + "\t" + str(vertex.element()) + "\t" + str(cost))


def testCorkCity(timeData=False):
    ids = {}

    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634

    if timeData:
        startTime = time.gmtime()
        startSecs = time.time()
    # Part 2 method - uses static method, so must reference RouteMap
    graph = RouteMap.graphReaderCorkCity("corkCityData.txt")
    # Part 1 method - much slower due to linear search for getting vertex reference
    # graph=Graph.graphReaderFormatOne("corkCityData.txt")
    graph.sp(ids["wgb"], ids['neptune'], label=True, printPath=True)
    if timeData:
        endTime = time.gmtime()
        endSecs = time.time()
        print("**** Time data ****\nStarted: " + time.asctime(startTime) + "\nEnded: " + time.asctime(endTime) + "\nTotal time (secs): " + str(endSecs-startSecs))

# gets route from wgb to neptune, to change route, see line 774.
testCorkCity(timeData=False)

