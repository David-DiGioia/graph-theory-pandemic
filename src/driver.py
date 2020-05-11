# This is the driver file, so we can do the startup work of the program here,
# like instantiating a graph and initializing a window to show graphics in
import pygame
import graph
import graphics
import data
import datetime

# This draws the drawable objects to the screen every frame
def render(screen):
    screen.fill(data.bg_color)
    for dv_id, dv in data.drawable_vertices.items():
        dv.draw_edges(screen, data.main_graph, data.drawable_vertices)
    for dv_id, dv in data.drawable_vertices.items():
        dv.draw(screen, data.main_graph)
    for button in data.buttons:
        button.draw(screen)
    for ib in data.input_boxes:
        ib.draw(screen)
    graphics.display_variables(screen, (data.WIDTH - 100, 25))
    pygame.display.flip()


# Creates both a drawable vertex and a logical vertex
def make_vertex(pos):
    v = graph.Vertex()
    data.main_graph.add_vertex(v)
    vd = graphics.VertexDrawable(v.id, pos)
    data.drawable_vertices[v.id] = vd


# Deletes drawable and logical vertex
def delete_vertex(v_id):
    data.main_graph.delete_vertex(v_id)
    del data.drawable_vertices[v_id]

def write_to_file():
    f = open("disease_output","a")
    f.write("\n" + str(datetime.datetime.now()))
    f.write("\nThe completion dates are " + str(data.completed_on))
    f.close()


# These three functions determine what happens when buttons are clicked on screen
def button_vertex_callback():
    data.mode = 0


# Button callback function
def button_edge_callback():
    data.mode = 1


# Button callback function
def button_infect_callback():
    data.mode = 2


# Button callback function
def button_step_callback():
    graph.spread_disease(data.main_graph, data.p)


# Button callback function
def button_test_callback():
    graph.test_graph(data.main_graph)

# Button callback function
def button_play_callback():
    graph.spread_disease_all(data.main_graph, data.p)
    data.completed_on.append(graph.current_day)

# Button callback function
def button_reset_today():
    graph.current_day = 0

# Button callback function
def button_list_dates():
    print("The completion dates are ")
    print(data.completed_on)

# Button callback function
def button_copy_run():
    graph.spread_disease_multi(data.main_graph,data.p,data.d,data.repeats)

def button_record_dates():
    write_to_file()


# InputBox callback function
def input_box_p_callback(text):
    try:
        data.p = float(text)
    except:
        print("Invalid input for p entered")


# InputBox callback function
def input_box_d_callback(text):
    try:
        data.d = int(text)
    except:
        print("Invalid input for d entered")

def input_box_repeats_callback(text):
    try:
        data.repeats = int(text)
    except:
        print("Invalid input for repeats entered")

# Deselect all vertices
def deselect_all():
    global selected_vertex
    selected_vertex = None
    for dv_id, dv in data.drawable_vertices.items():
        dv.selected = False


# In vertex mode we can make/delete vertices when we click
def click_vertex_mode(pos):
    for dv_id, dv in data.drawable_vertices.items():
        # Have we clicked on one of the vertices?
        if dv.collide_point(pos):
            delete_vertex(dv_id)
            return
    make_vertex(pos)


# In edge mode we can make/delete edges when we click
def click_edge_mode(pos):
    global selected_vertex
    clicked_vertex = False
    for dv_id, dv in data.drawable_vertices.items():
        # Have we clicked on one of the vertices?
        if dv.collide_point(pos):
            clicked_vertex = True
            # If we've already selected one vertex, then make/delete an edge between the two selected
            if selected_vertex is not None:
                # If an edge already exists, we'll delete it
                if data.main_graph.adjacent(dv_id, selected_vertex.id):
                    data.main_graph.delete_edge(dv_id, selected_vertex.id)
                # Otherwise we make a new edge
                else:
                    data.main_graph.make_edge(dv_id, selected_vertex.id)
                deselect_all()
            else:
                dv.selected = True
                selected_vertex = dv
            break
    if not clicked_vertex:
        deselect_all()


# In infect mode we can infect/disinfect vertices when we click
def click_infect_mode(pos):
    for dv_id, dv in data.drawable_vertices.items():
        # Have we clicked on one of the vertices?
        if dv.collide_point(pos):
            if data.main_graph.get_vertex(dv_id).infected:
                data.main_graph.disinfect_vertex(dv.id)
            else:
                data.main_graph.infect_vertex(dv.id)
            break


# When user clicks screen, this function determines what happens depending on which mode is active
def handle_click(pos):
    global active_input_box
    clicked_button = None
    for button in data.buttons:
        if button.rect.collidepoint(pos):
            clicked_button = button

    if clicked_button is not None:
        clicked_button.click_event(data.buttons)

    clicked_input_box = None
    for ib in data.input_boxes:
        if ib.rect.collidepoint(pos):
            clicked_input_box = ib

    if clicked_input_box is None:
        for ib in data.input_boxes:
            ib.selected = False

    if clicked_input_box is not None:
        clicked_input_box.click_event(data.input_boxes)
        active_input_box = clicked_input_box

    # If we haven't clicked a button, then what we do next depends on what mode we're in
    elif data.mode == 0:
        click_vertex_mode(pos)
    elif data.mode == 1:
        click_edge_mode(pos)
    elif data.mode == 2:
        click_infect_mode(pos)


# for debug
def print_current_day():
    print("Today is day " + str(graph.current_day))


# Create the clickable gui buttons which appear on screen
def make_buttons():
    button_vertical_spacing = 60
    data.buttons.append(graphics.Button((20, 20), "Vertex Mode", button_vertex_callback))
    data.buttons[0].selected = True
    data.buttons.append(graphics.Button((20, 20 + button_vertical_spacing), "Edge Mode", button_edge_callback))
    data.buttons.append(graphics.Button((20, 20 + 2*button_vertical_spacing), "Infect Mode", button_infect_callback))
    data.buttons.append(graphics.Button((20, 20 + 3*button_vertical_spacing), "Step", button_step_callback, False))
    data.buttons.append(graphics.Button((20, 20 + 4*button_vertical_spacing), "TEST", button_test_callback, False))
    data.buttons.append(graphics.Button((20, 20 + 5*button_vertical_spacing), "Play Infection", button_play_callback, False))
    data.buttons.append(graphics.Button((20, 20 + 6*button_vertical_spacing), "List of Dates", button_list_dates, False))
    data.buttons.append(graphics.Button((20, 20 + 7* button_vertical_spacing), "Run multiple times", button_copy_run, False))
    data.buttons.append(graphics.Button((20, 20 + 8* button_vertical_spacing), "Write it down", button_record_dates, False))
    data.input_boxes.append(graphics.InputBox((data.WIDTH - 140, 160), input_box_p_callback))
    data.input_boxes.append(graphics.InputBox((data.WIDTH - 140, 210), input_box_d_callback))
    data.input_boxes.append(graphics.InputBox((data.WIDTH - 140, 260), input_box_repeats_callback))



def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Graph Theory Epidemic")
    screen = pygame.display.set_mode((data.WIDTH, data.HEIGHT))
    graphics.init_graphics()
    make_buttons()

    # Make new graph
    data.main_graph = graph.Graph()

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

            if event.type == pygame.KEYDOWN:
                if active_input_box is not None and active_input_box.selected:
                    active_input_box.key_event(event)


# run the driver.py function only if this module is executed as the driver.py script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
