# Here we can write any data structures related to graphs and all the functionality that goes with it


vertexId = 0


class Vertex:
    def __init__(self, infected=False, adjacent=None):
        global vertexId

        # Is this vertex infected?
        self.infected = infected

        # adjacentVertices is a set of all vertices' IDs which are adjacent to this one
        if adjacent is None:
            self.adjacentVertices = set()
        else:
            self.adjacentVertices = adjacent

        # Assign a unique id to this vertex (so that we can reference it later)
        self.id = vertexId
        vertexId += 1


class Graph:
    def __init__(self):
        # vertices is a dictionary associating the each vertex's id number with the vertex
        self.vertices = {}
        # frontier is a set containing all vertices which have potential to infect other vertices.
        # That is, it contains each infected vertex with uninfected adjacent vertices
        self.frontier = set()

    def add_vertex(self, vertex):
        # Make the vertex's id number the key to accessing the vertex in the dictionary
        self.vertices[vertex.id] = vertex

    def make_edge(self, v1, v2):
        # Since this is an undirected graph, we add the vertices to each other's list of adjacent vertices
        self.vertices[v1].adjacentVertices.add(v2)
        self.vertices[v2].adjacentVertices.add(v1)

    def update_frontier(self):
        for vertex in self.frontier:
            for adjacent in vertex.adjacentVertices:
                if not adjacent.infected:
                    break
            # If all vertices adjacent to vertex are infected already, remove vertex from the frontier
            self.frontier.remove(vertex)

    def infect_vertex(self, vertex):
        vertex.infected = True
        self.frontier.add(vertex)
        self.update_frontier()

    def get_vertex(self, id):
        return self.vertices[id]
