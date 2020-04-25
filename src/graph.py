# Here we can write any data structures related to graphs and all the functionality that goes with it
import random
import copy
import data

vertex_id_current = 0
current_day = 0


# Until we make some more controls on screen, you can use this to test ideas with the graph
# that you create when running the program
def test_graph(graph):
    print("Test graph called!")
    # graph refers to the graph object that you made on screen.
    # You can access all of it's vertices using graph.vertices, which is a dictionary of the form
    # { vertex_id : vertex }. In other words, the key is a vertex_id and the value is the actual vertex.
    # We use a vertex_id bc it's helpful sometimes when you need to refer to the vertex but you can just loop
    # through all the vertices and use the vertex data without worrying about the key if you want, like this:
    for vertex_id, vertex in graph.vertices.items():
        print("The id of this vertex is " + str(vertex_id) + ", and this vertex's infected status is: " + str(vertex.infected))
    print("")

    # And the graph also has a member called frontier, which is just the set of vertices which have potential to
    # infect other vertices. In other words, it is the set of infected vertices which is connected by an edge to at
    # least 1 non-infected vertex.
    print("Graph's frontier:")
    for vertex in graph.frontier:
        print("Vertex with id " + str(vertex.id) + " is a member of the graph's frontier.")
    print("")

    # Each vertex has the following data members: infected, adjacent_vertices, and id.
    # Infected is just a boolean telling whether or not the vertex is infected.
    # adjacent_vertices is a set of vertex id's which are adjacent to this vertex. In other words, they share an
    # edge with one another. This is what defines the edges in the graph.
    for vertex_id, vertex in graph.vertices.items():
        print("Vertex with id " + str(vertex_id) + " is connected to vertices with the following IDs:")
        for adjacent_vertex_id in vertex.adjacent_vertices:
            print(adjacent_vertex_id)


# Spread the disease with probability p
def spread_disease(graph, p):
    global current_day
    current_day += 1
    # We make a copy of the vertices so that a vertex infected this timestep can not
    # infect other vertices until the next time step
    vertices_copy = copy.deepcopy(graph.vertices)
    for v_id, v in vertices_copy.items():
        if v.infected:
            graph.vertices[v_id].heal_days += 1
            if graph.vertices[v_id].heal_days == data.d:
                graph.disinfect_vertex(v_id)
                graph.vertices[v_id].heal_days = 0
            for adj_id in v.adjacent_vertices:
                # If the adjacent vertex is not infected, there is a p chance they become infected
                if not graph.vertices[adj_id].infected:
                    if random.random() <= p:
                        graph.infect_vertex(adj_id)


def spread_disease_all(graph, p):
    while len(graph.frontier) > 0:
        spread_disease(graph, p)


class Vertex:
    def __init__(self, infected=False, adjacent=None):
        global vertex_id_current

        # Is this vertex infected?
        self.infected = infected

        # How long does it take this vertex to heal?
        self.heal_days = 0

        # adjacentVertices is a set of all vertices' IDs which are adjacent to this one
        if adjacent is None:
            self.adjacent_vertices = set()
        else:
            self.adjacent_vertices = adjacent

        # Assign a unique id to this vertex (so that we can reference it later)
        self.id = vertex_id_current
        vertex_id_current += 1


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

    def delete_vertex(self, v_id):
        # Remove the edges connecting to this vertex
        for adj_id in self.vertices[v_id].adjacent_vertices:
            self.vertices[adj_id].adjacent_vertices.remove(v_id)
        del self.vertices[v_id]

    def make_edge(self, v1, v2):
        # Since this is an undirected graph, we add the vertices to each other's list of adjacent vertices
        self.vertices[v1].adjacent_vertices.add(v2)
        self.vertices[v2].adjacent_vertices.add(v1)

    def delete_edge(self, v1_id, v2_id):
        self.vertices[v1_id].adjacent_vertices.remove(v2_id)
        self.vertices[v2_id].adjacent_vertices.remove(v1_id)

    # Are these two vertices connected by an edge?
    def adjacent(self, v1_id, v2_id):
        return v2_id in self.vertices[v1_id].adjacent_vertices

    def update_frontier_infect(self):
        for vertex in self.frontier.copy():
            has_healthy_neighbor = False
            for adjacent in vertex.adjacent_vertices:
                if not self.vertices[adjacent].infected:
                    has_healthy_neighbor = True
                    break
                # If all vertices adjacent to vertex are infected already, remove vertex from the frontier
            if not has_healthy_neighbor:
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
