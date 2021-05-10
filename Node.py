class Node:

    def __init__(self):
        self.parents = []

    def get_parents(self):
        return self.parents

    def remove_parent(self, parent):
        self.parents.remove(parent)

    def add_parent(self, parent):
        self.parents.append(parent)

    def replace_self(self, other):
        for i in range(len(self.parents)):
            self.parents[0].swap_child(self, other)
            
        if len(self.parents) > 0:
            raise ValueError("Error in node replacement, parents not empty")


