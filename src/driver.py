# This is the driver file, so we can do the startup work of the program here,
# like instantiating a graph and initializing a window to show graphics in
import pygame
from graph import *
from graphics import *


# width and height of the screen
WIDTH = 640
HEIGHT = 480
graph = None
drawable_objects = []


def render(screen):
    screen.fill((150, 150, 150))
    for do in drawable_objects:
        do.draw(screen, graph)
    pygame.display.flip()


def main():
    global graph
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Graph Theory Epidemic")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Make new graph
    graph = Graph()

    # Populate graph with 5 vertices which are unconnected to each other
    for i in range(5):
        v = Vertex()
        graph.add_vertex(v)
        vd = VertexDrawable(v.id, (i * 40, 100))
        drawable_objects.append(vd)

    # Make an edge between the vertex with id=1 and the vertex with id=2
    graph.make_edge(0, 1)

    graph.infect_vertex(1)

    # Vertex with id=0 has 1 adjacent vertex since we just made an edge connected to it
    print("Vertex with id=1 has this many adjacent vertices: " + str(len(graph.vertices[0].adjacent_vertices)))

    running = True
    # main loop
    while running:
        render(screen)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


# run the driver.py function only if this module is executed as the driver.py script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
