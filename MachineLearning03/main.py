import pygame
from pygame.locals import *


class Node:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.radius = 20
        self.color = (255, 255, 255)
        self.connections = []
        self.dragging = False

    def add_connection(self, node):
        self.connections.append(node)

    def delete_connection(self, node):
        self.connections.remove(node)

    def draw(self, screen):
        # Draw the node as a circle
        pygame.draw.circle(screen, self.color, self.position, self.radius)

        # Draw lines to represent connections
        for neighbor in self.connections:
            pygame.draw.line(screen, self.color, self.position, neighbor.position)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # Left-click: Start dragging the node
                mouse_pos = pygame.mouse.get_pos()
                if self.distance_to(mouse_pos) <= self.radius:
                    self.dragging = True
            elif event.button == 3:
                # Right-click: Add/delete connection
                mouse_pos = pygame.mouse.get_pos()
                if self.distance_to(mouse_pos) <= self.radius:
                    selected_node = self.get_selected_node(mouse_pos)
                    if selected_node:
                        if selected_node in self.connections:
                            self.delete_connection(selected_node)
                        else:
                            self.add_connection(selected_node)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                # Left-click release: Stop dragging the node
                self.dragging = False

        elif event.type == MOUSEMOTION:
            # Mouse movement: Update node position if dragging
            if self.dragging:
                mouse_pos = pygame.mouse.get_pos()
                self.position = mouse_pos

    def distance_to(self, point):
        dx = self.position[0] - point[0]
        dy = self.position[1] - point[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    def get_selected_node(self, point):
        for node in nodes:
            if node != self and self.distance_to(node.position) <= self.radius:
                return node
        return None


# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Node Connections')

# Create nodes
node1 = Node('A', (100, 100))
node2 = Node('B', (200, 200))
node3 = Node('C', (300, 300))
node4 = Node('D', (400, 400))

# Add connections between nodes
node1.add_connection(node2)
node1.add_connection(node3)
node2.add_connection(node3)
node2.add_connection(node4)
node3.add_connection(node4)

# Create a list to hold the nodes
nodes = [node1, node2, node3, node4]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Handle events for each node
        for node in nodes:
            node.handle_event(event)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the nodes and connections
    for node in nodes:
        node.draw(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
