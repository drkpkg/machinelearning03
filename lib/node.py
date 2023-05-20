import pygame
from pygame.locals import *

from lib.event_manager import EventManager
from lib.graph import Graph


class Node:
    event_manager = EventManager()
    nodes = []

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.radius = 20
        self.color = (255, 255, 255)
        self.connections = []
        self.dragging = False
        self.selected = False

        # Register event listeners
        Node.event_manager.add_listener(MOUSEBUTTONDOWN, self.handle_mouse_button_down)
        Node.event_manager.add_listener(MOUSEBUTTONUP, self.handle_mouse_button_up)
        Node.event_manager.add_listener(MOUSEMOTION, self.handle_mouse_motion)

        Node.nodes.append(self)

    def add_connection(self, node, weight):
        if node not in [connection[0] for connection in self.connections]:
            self.connections.append((node, weight))
            node.connections.append((self, weight))

    def delete_connection(self, node):
        for connection in self.connections:
            if connection[0] == node:
                self.connections.remove(connection)
                node.connections.remove((self, connection[1]))

    def draw(self, screen):
        # Draw the node as a circle
        if self.selected:
            color = (0, 0, 255)  # Blue if selected
        else:
            color = self.color

        pygame.draw.circle(screen, color, self.position, self.radius)

        # Draw lines to represent connections
        for neighbor, weight in self.connections:
            pygame.draw.line(screen, color, self.position, neighbor.position)

            # Render and display the weight
            font = pygame.font.Font(None, 18)
            text = font.render(str(weight), True, (0, 0, 0))
            text_rect = text.get_rect(center=((self.position[0] + neighbor.position[0]) // 2,
                                              (self.position[1] + neighbor.position[1]) // 2))
            screen.blit(text, text_rect)

        # Render and display the letter
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)

    def handle_mouse_button_down(self, event):
        if event.button == 1:
            # Left-click: Start dragging the node
            mouse_pos = pygame.mouse.get_pos()
            if self.distance_to(mouse_pos) <= self.radius:
                self.dragging = True
                self.selected = not self.selected  # Toggle selection on click
        elif event.button == 3:
            # Right-click: Add/delete connection
            mouse_pos = pygame.mouse.get_pos()
            if self.distance_to(mouse_pos) <= self.radius:
                selected_node = self.get_selected_node(mouse_pos)
                if selected_node:
                    if selected_node in [connection[0] for connection in self.connections]:
                        self.delete_connection(selected_node)
                    else:
                        self.add_connection(selected_node)

    def handle_mouse_button_up(self, event):
        if event.button == 1:
            # Left-click release: Stop dragging the node
            self.dragging = False

    def handle_mouse_motion(self, event):
        # Mouse movement: Update node position if dragging
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.position = mouse_pos

    def distance_to(self, point):
        dx = self.position[0] - point[0]
        dy = self.position[1] - point[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    def get_selected_node(self, point):
        for node in Node.nodes:
            if node != self and self.distance_to(node.position) <= self.radius:
                return node
        return None

    def breadth_first_search(self, goal):
        graph = self.create_graph()
        return graph.breadth_first_search(self.name, goal.name)

    def depth_first_search(self, goal):
        graph = self.create_graph()
        return graph.depth_first_search(self.name, goal.name)

    def dijkstra(self, goal):
        graph = self.create_graph()
        return graph.dijkstra(self.name, goal.name)

    def create_graph(self):
        graph = Graph()

        for node in Node.nodes:
            for neighbor, weight in node.connections:
                graph.add_edge(node.name, neighbor.name, weight)

        return graph
