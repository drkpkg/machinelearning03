class NodeManager:
    _instance = None

    def __init__(self):
        if NodeManager._instance is not None:
            raise Exception("NodeManager is a singleton class. Use NodeManager.get_instance() to access the instance.")
        self.nodes = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NodeManager()
        return cls._instance

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def get_nodes(self):
        return self.nodes