# This file contains the code related to what will be displayed on the screen
import pygame
import pygame.freetype


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


# Return the squared distance between loc1 and loc2
def distance_squared(loc1, loc2):
    x = loc2[0] - loc1[0]
    y = loc2[1] - loc1[1]
    return x*x + y*y


def init_graphics():
    global button_font
    button_font = pygame.freetype.SysFont("Times New Roman", 20)


# Contains all the information needed to draw a vertex to the screen
class VertexDrawable:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.selected = False
        self.radius = vertex_radius

    def draw(self, screen, graph):
        # Draw infected vertices as different color than healthy ones
        if self.selected:
            color = selected_color
        elif graph.get_vertex(self.id).infected:
            color = infected_color
        else:
            color = healthy_color
        pygame.draw.circle(screen, color, self.location, vertex_radius)

    # Returns true if pos lies inside this vertex's circle on screen
    def collide_point(self, pos):
        return distance_squared(pos, self.location) <= self.radius * self.radius


class Button:
    def __init__(self, location, text, call_back=None):
        self.location = location
        self.text = text
        self.selected = False
        self.rect = pygame.Rect(self.location[0], self.location[1], 120, 40)
        self.call_back = call_back

    def draw(self, screen):
        global button_font
        if self.selected:
            color = button_color_selected
        else:
            color = button_color
        pygame.draw.rect(screen, color, self.rect)
        button_font.render_to(screen, self.location, self.text)

    def click_event(self):
        if self.call_back is not None:
            self.call_back()
        self.selected = True
