class Node:
    def __init__(self, pos):
        self.pos = pos
        self.parent = None
        self.g_cost = None
        self.h_cost = None
        self.total_cost = None
        self.diagonal = False

    def __eq__(self, other):
        return self.pos == other.pos
