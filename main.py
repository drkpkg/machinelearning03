import pygame
from pygame.locals import *
import random

from lib.node import Node
from lib.node_manager import NodeManager

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Node Connections')

# Create the NodeManager instance
node_manager = NodeManager.get_instance()

# Generate random nodes
num_nodes = 10
nodes = []
for i in range(num_nodes):
    name = chr(65 + i)  # A, B, C, ...
    position = (random.randint(100, 700), random.randint(100, 500))
    node = Node(name, position)
    nodes.append(node)
    node_manager.add_node(node)

# Generate random connections with random weights
max_connections = 3  # Maximum number of connections per node
for node in nodes:
    num_connections = random.randint(1, max_connections)
    connected_nodes = random.sample(nodes, num_connections)
    for connected_node in connected_nodes:
        if connected_node != node:
            weight = random.randint(1, 10)
            node.add_connection(connected_node, weight)

# Main loop
running = True
selected_node = None
target_node = None

# Help message
font = pygame.font.Font(None, 24)
help_text = font.render("Press 'S' to select a node. Press 'T' to set the target node.", True, (0, 0, 0))
help_text_rect = help_text.get_rect(center=(screen.get_width() // 2, 30))

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Dispatch events to the event manager
        Node.event_manager.dispatch(event)

        if event.type == KEYDOWN:
            if event.key == K_s:
                # Press 'S' to select a node
                mouse_pos = pygame.mouse.get_pos()
                for node in node_manager.get_nodes():
                    if node.distance_to(mouse_pos) <= node.radius:
                        selected_node = node
                        target_node = None

            if event.key == K_t and selected_node:
                # Press 'T' to set the target node
                mouse_pos = pygame.mouse.get_pos()
                for node in node_manager.get_nodes():
                    if node.distance_to(mouse_pos) <= node.radius:
                        target_node = node

    # Clear the screen
    screen.fill((100, 200, 255))

    # Draw the nodes and connections
    for node in node_manager.get_nodes():
        node.draw(screen)

    # Display help message
    screen.blit(help_text, help_text_rect)

    # Display route information
    if selected_node and target_node:
        dijkstra_route = selected_node.dijkstra(target_node)
        depth_first_route = selected_node.depth_first_search(target_node)
        breadth_first_route = selected_node.breadth_first_search(target_node)

        route_text = font.render(f"Dijkstra: {dijkstra_route}   Depth First Search: {depth_first_route}   Breadth First Search: {breadth_first_route}",
                                 True, (0, 0, 0))
        route_text_rect = route_text.get_rect(center=(screen.get_width() // 2, 60))
        screen.blit(route_text, route_text_rect)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
