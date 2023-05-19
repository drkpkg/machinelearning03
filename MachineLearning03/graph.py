import heapq


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}
        self.graph[u][v] = weight
        self.graph[v][u] = weight

    def get_shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        # Priority queue to keep track of nodes to visit
        queue = [(0, start)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            # Ignore if already found a shorter path to current_node
            if current_distance > distances[current_node]:
                continue

            # Check each neighbor of the current_node
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                # Update distance if a shorter path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        # Reconstruct the shortest path
        path = []
        current_node = end

        while current_node != start:
            path.append(current_node)
            current_node = min(
                self.graph[current_node],
                key=lambda node: distances[node] + self.graph[node][current_node]
            )

        path.append(start)
        path.reverse()

        return path, distances[end]
