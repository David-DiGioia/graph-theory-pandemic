# This is the driver file, so we can do the startup work of the program here,
# like instantiating a graph and initializing a window to show graphics in
import pygame
from graph import *
from graphics import *


# width and height of the screen
WIDTH = 1280
HEIGHT = 720
# Background color of the screen
bg_color = (80, 80, 80)
# Main graph we will be manipulating
graph = None
# The vertex objects and buttons that will be drawn to screen
drawable_vertices = []
buttons = []
# Mode types are as follows: vertex=0, edge=1, infect=2
# The mode determines what happens when you click on screen (inserting vertices/edges, or infecting vertices)
mode = 0


# This draws the drawable objects to the screen every frame
def render(screen):
    screen.fill(bg_color)
    for dv in drawable_vertices:
        dv.draw(screen, graph)
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()


# Creates both a drawable vertex and a logical vertex
def make_vertex(pos):
    v = Vertex()
    graph.add_vertex(v)
    vd = VertexDrawable(v.id, pos)
    drawable_vertices.append(vd)


# These three functions determine what happens when buttons are clicked on screen
def button_vertex_callback():
    global mode
    mode = 0


def button_edge_callback():
    global mode
    mode = 1


def button_infect_callback():
    global mode
    mode = 2


def main():
    global graph
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Graph Theory Epidemic")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    init_graphics()

    button_vertical_spacing = 60
    buttons.append(Button((20, 20), "Vertex Mode", button_vertex_callback))
    buttons[0].selected = True
    buttons.append(Button((20, 20 + button_vertical_spacing), "Edge Mode", button_edge_callback))
    buttons.append(Button((20, 20 + 2*button_vertical_spacing), "Infect Mode", button_infect_callback))

    # Make new graph
    graph = Graph()

    # main loop
    running = True
    while running:
        render(screen)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                clicked_button = None
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        clicked_button = button

                if clicked_button is not None:
                    for button in buttons:
                        button.selected = False
                    clicked_button.click_event()
                # vertex mode
                elif mode == 0:
                    make_vertex(pos)
                # edge mode
                elif mode == 1:
                    pass
                # infect mode
                elif mode == 2:
                    pass

            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


# run the driver.py function only if this module is executed as the driver.py script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
