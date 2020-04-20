# DRIVER DATA --------------------------------------------------------------------------------------------
# width and height of the screen
WIDTH = 1280
HEIGHT = 720
# Background color of the screen
bg_color = (80, 80, 80)
# Main graph we will be manipulating
main_graph = None
# The vertex objects and buttons that will be drawn to screen
drawable_vertices = {}
buttons = []
input_boxes = []
active_input_box = None
# Mode types are as follows: vertex=0, edge=1, infect=2
# The mode determines what happens when you click on screen (inserting vertices/edges, or infecting vertices)
mode = 0
# Which vertex is currently selected by user?
selected_vertex = None
# What is the probability of the disease spreading on each edge?
p = 0.2
# --------------------------------------------------------------------------------------------------------

# GRAPHICS DATA --------------------------------------------------------------------------------------------
# Radius of vertices in pixels
vertex_radius = 10
# Color of healthy vertices
healthy_color = (0, 255, 0)
# Color of infected vertices
infected_color = (255, 0, 0)
# Color of selected vertices
selected_color = (255, 255, 255)
# Font to be used in button ui
button_font = None
button_color = (150, 150, 150)
button_color_selected = (110, 110, 110)
input_box_color = (200, 200, 200)
input_box_color_selected = (255, 255, 255)
edge_color = (0, 0, 0)
edge_thickness = 3
# --------------------------------------------------------------------------------------------------------
