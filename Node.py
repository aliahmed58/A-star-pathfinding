class Node:
    # Node class ctor that takes in a position
    def __init__(self, x: int, y: int):
        # set position and init other values to default
        self.x = x
        self.y = y
        self.parent = None
        self.g_cost = 0
        self.h_cost = 0
        self.total_cost = 0
        self.diagonal = False

    # override equal function for equality check in a list
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
