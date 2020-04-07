# This file contains the code related to what will be displayed on the screen
import pygame


# Radius of vertices in pixels
vertex_radius = 10
# Color of healthy vertices
healthy_color = (0, 255, 0)
# Color of infected vertices
infected_color = (255, 0, 0)


class VertexDrawable:
    def __init__(self, id, location):
        self.id = id
        self.location = location

    def draw(self, screen, graph):
        # Draw infected vertices as different color than healthy ones
        if graph.get_vertex(self.id).infected:
            color = infected_color
        else:
            color = healthy_color
        pygame.draw.circle(screen, color, self.location, vertex_radius)
