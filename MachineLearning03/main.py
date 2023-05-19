from graph import Graph


if __name__ == '__main__':
    graph = Graph()

    # Add edges
    graph.add_edge('A', 'B', 5)
    graph.add_edge('A', 'C', 2)
    graph.add_edge('B', 'C', 1)
    graph.add_edge('B', 'D', 3)
    graph.add_edge('C', 'D', 4)
    graph.add_edge('C', 'E', 6)
    graph.add_edge('D', 'E', 2)

    # Find the shortest path from 'A' to 'E'
    path, distance = graph.get_shortest_path('A', 'E')

    print("Shortest Path:", path)
    print("Distance:", distance)
