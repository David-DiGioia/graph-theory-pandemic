# This file contains the code related to what will be displayed on the screen
import pygame
import pygame.freetype
import graph
import driver
import data


# Return the squared distance between loc1 and loc2
def distance_squared(loc1, loc2):
    x = loc2[0] - loc1[0]
    y = loc2[1] - loc1[1]
    return x*x + y*y


def init_graphics():
    data.button_font = pygame.freetype.SysFont("Times New Roman", 20)


def display_variables(screen, pos):
    vertical_spacing = 20
    data.button_font.render_to(screen, pos, "Day: " + str(graph.current_day))
    data.button_font.render_to(screen, (pos[0], pos[1] + vertical_spacing), "p:      " + str(data.p))
    data.button_font.render_to(screen, (data.WIDTH - 140, 80), "Adjust p value:")


# Contains all the information needed to draw a vertex to the screen
class VertexDrawable:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.selected = False
        self.radius = data.vertex_radius

    def draw(self, screen, graph):
        # Draw infected vertices as different color than healthy ones
        if self.selected:
            color = data.selected_color
        elif graph.get_vertex(self.id).infected:
            color = data.infected_color
        else:
            color = data.healthy_color
        pygame.draw.circle(screen, color, self.location, data.vertex_radius)

    def draw_edges(self, screen, graph, drawable_vertices):
        for adj_id in graph.get_vertex(self.id).adjacent_vertices:
            pygame.draw.line(screen, data.edge_color, self.location, drawable_vertices[adj_id].location, data.edge_thickness)

    # Returns true if pos lies inside this vertex's circle on screen
    def collide_point(self, pos):
        return distance_squared(pos, self.location) <= self.radius * self.radius


class Button:
    def __init__(self, location, text, call_back=None, selectable=True):
        self.location = location
        self.text = text
        self.selected = False
        self.rect = pygame.Rect(self.location[0], self.location[1], 120, 40)
        self.call_back = call_back
        self.selectable = selectable

    def draw(self, screen):
        global button_font
        if self.selected:
            color = data.button_color_selected
        else:
            color = data.button_color
        pygame.draw.rect(screen, color, self.rect)
        data.button_font.render_to(screen, self.location, self.text)

    def click_event(self, buttons):
        if self.call_back is not None:
            self.call_back()
        if self.selectable:
            for button in buttons:
                button.selected = False
            self.selected = True


class InputBox:
    def __init__(self, location, call_back=None):
        self.location = location
        self.text = ""
        self.selected = False
        self.rect = pygame.Rect(self.location[0], self.location[1], 120, 20)
        self.call_back = call_back

    def draw(self, screen):
        global button_font
        if self.selected:
            color = data.input_box_color_selected
        else:
            color = data.input_box_color
        pygame.draw.rect(screen, color, self.rect)
        data.button_font.render_to(screen, self.location, self.text)

    def click_event(self, input_boxes):
        for ib in input_boxes:
            ib.selected = False
        self.selected = True

    def key_event(self, event):
        if event.key == pygame.K_RETURN:
            self.call_back(self.text)
            self.text = ''
            self.selected = False
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
