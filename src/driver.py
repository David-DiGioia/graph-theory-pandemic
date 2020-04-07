# This is the driver file, so we can do the startup work of the program here,
# like instantiating a graph and initializing a window to show graphics in
from graph import *


def main():
    # Make new graph
    graph = Graph()

    # Populate graph with 5 vertices which are unconnected to each other
    for i in range(5):
        graph.add_vertex(Vertex())

    # Make an edge between the vertex with id=1 and the vertex with id=2
    graph.make_edge(0, 1)

    # Vertex with id=0 has 1 adjacent vertex since we just made an edge connected to it
    print("Vertex with id=1 has this many adjacent vertices: " + str(len(graph.vertices[0].adjacentVertices)))


# run the driver.py function only if this module is executed as the driver.py script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
