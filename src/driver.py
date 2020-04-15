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
drawable_vertices = {}
buttons = []
# Mode types are as follows: vertex=0, edge=1, infect=2
# The mode determines what happens when you click on screen (inserting vertices/edges, or infecting vertices)
mode = 0
selected_vertex = None


# This draws the drawable objects to the screen every frame
def render(screen):
    screen.fill(bg_color)
    for dv_id, dv in drawable_vertices.items():
        dv.draw_edges(screen, graph, drawable_vertices)
    for dv_id, dv in drawable_vertices.items():
        dv.draw(screen, graph)
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()


# Creates both a drawable vertex and a logical vertex
def make_vertex(pos):
    v = Vertex()
    graph.add_vertex(v)
    vd = VertexDrawable(v.id, pos)
    drawable_vertices[v.id] = vd


# Deletes drawable and logical vertex
def delete_vertex(v_id):
    graph.delete_vertex(v_id)
    del drawable_vertices[v_id]


# These three functions determine what happens when buttons are clicked on screen
def button_vertex_callback():
    global mode
    mode = 0


# Button callback function
def button_edge_callback():
    global mode
    mode = 1


# Button callback function
def button_infect_callback():
    global mode
    mode = 2


# Button callback function
def button_test_callback():
    test_graph(graph)


# Deselect all vertices
def deselect_all():
    global selected_vertex
    selected_vertex = None
    for dv_id, dv in drawable_vertices.items():
        dv.selected = False


# In vertex mode we can make/delete vertices when we click
def click_vertex_mode(pos):
    for dv_id, dv in drawable_vertices.items():
        # Have we clicked on one of the vertices?
        if dv.collide_point(pos):
            delete_vertex(dv_id)
            return
    make_vertex(pos)


# In edge mode we can make/delete edges when we click
def click_edge_mode(pos):
    global selected_vertex
    clicked_vertex = False
    for dv_id, dv in drawable_vertices.items():
        # Have we clicked on one of the vertices?
        if dv.collide_point(pos):
            clicked_vertex = True
            # If we've already selected one vertex, then make/delete an edge between the two selected
            if selected_vertex is not None:
                # If an edge already exists, we'll delete it
                if graph.adjacent(dv_id, selected_vertex.id):
                    graph.delete_edge(dv_id, selected_vertex.id)
                # Otherwise we make a new edge
                else:
                    graph.make_edge(dv_id, selected_vertex.id)
                deselect_all()
            else:
                dv.selected = True
                selected_vertex = dv
            break
    if not clicked_vertex:
        deselect_all()


# In infect mode we can infect/disinfect vertices when we click
def click_infect_mode(pos):
    for dv_id, dv in drawable_vertices.items():
        # Have we clicked on one of the vertices?
        if dv.collide_point(pos):
            if graph.get_vertex(dv_id).infected:
                graph.disinfect_vertex(dv.id)
            else:
                graph.infect_vertex(dv.id)
            break


# When user clicks screen, this function determines what happens depending on which mode is active
def handle_click(pos):
    clicked_button = None
    for button in buttons:
        if button.rect.collidepoint(pos):
            clicked_button = button

    if clicked_button is not None:
        clicked_button.click_event(buttons)

    # If we haven't clicked a button, then what we do next depends on what mode we're in
    elif mode == 0:
        click_vertex_mode(pos)
    elif mode == 1:
        click_edge_mode(pos)
    elif mode == 2:
        click_infect_mode(pos)


# Create the clickable gui buttons which appear on screen
def make_buttons():
    button_vertical_spacing = 60
    buttons.append(Button((20, 20), "Vertex Mode", button_vertex_callback))
    buttons[0].selected = True
    buttons.append(Button((20, 20 + button_vertical_spacing), "Edge Mode", button_edge_callback))
    buttons.append(Button((20, 20 + 2*button_vertical_spacing), "Infect Mode", button_infect_callback))
    buttons.append(Button((20, 20 + 3*button_vertical_spacing), "TEST", button_test_callback, False))


def main():
    global graph
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Graph Theory Epidemic")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    init_graphics()
    make_buttons()

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
                handle_click(pos)

            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


# run the driver.py function only if this module is executed as the driver.py script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
