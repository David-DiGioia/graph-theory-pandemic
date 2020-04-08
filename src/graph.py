# Here we can write any data structures related to graphs and all the functionality that goes with it


vertex_id = 0


class Vertex:
    def __init__(self, infected=False, adjacent=None):
        global vertex_id

        # Is this vertex infected?
        self.infected = infected

        # adjacentVertices is a set of all vertices' IDs which are adjacent to this one
        if adjacent is None:
            self.adjacent_vertices = set()
        else:
            self.adjacent_vertices = adjacent

        # Assign a unique id to this vertex (so that we can reference it later)
        self.id = vertex_id
        vertex_id += 1


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
        self.vertices[v1].adjacent_vertices.add(v2)
        self.vertices[v2].adjacent_vertices.add(v1)

    def update_frontier_infect(self):
        for vertex in self.frontier.copy():
            for adjacent in vertex.adjacent_vertices:
                if not self.vertices[adjacent].infected:
                    break
            # If all vertices adjacent to vertex are infected already, remove vertex from the frontier
            self.frontier.remove(vertex)

    def update_frontier_disinfect(self, vertex):
        for adj_id in vertex.adjacent_vertices:
            if self.vertices[adj_id].infected:
                self.frontier.add(self.vertices[adj_id])

    def infect_vertex(self, v_id):
        vertex = self.vertices[v_id]
        vertex.infected = True
        self.frontier.add(vertex)
        self.update_frontier_infect()

    def disinfect_vertex(self, v_id):
        vertex = self.vertices[v_id]
        vertex.infected = False
        self.frontier.discard(vertex)
        self.update_frontier_disinfect(vertex)

    def get_vertex(self, v_id):
        return self.vertices[v_id]
