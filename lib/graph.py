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

    def breadth_first_search(self, start, goal):
        queue = [(start, [start])]
        visited = set([start])
        weights = {node: 0 for node in self.graph}

        while queue:
            node, path = queue.pop(0)
            if node == goal:
                return path, weights[goal]
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    weights[neighbor] = weights[node] + self.graph[node][neighbor]

        return None, None


    def depth_first_search(self, start, goal):
        stack = [(start, [start])]
        visited = set([start])
        weights = {node: 0 for node in self.graph}

        while stack:
            node, path = stack.pop()
            if node == goal:
                return path, weights[goal]
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
                    weights[neighbor] = weights[node] + self.graph[node][neighbor]

        return None, None

    def dijkstra(self, start, goal):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        weights = {node: float('inf') for node in self.graph}
        weights[start] = 0

        queue = [(0, start)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    weights[neighbor] = weights[current_node] + weight
                    heapq.heappush(queue, (distance, neighbor))

        path = []
        current_node = goal

        while current_node != start:
            path.append(current_node)
            current_node = min(
                self.graph[current_node],
                key=lambda node: distances[node] + self.graph[node][current_node]
            )

        path.append(start)
        path.reverse()

        return path, weights[goal]
