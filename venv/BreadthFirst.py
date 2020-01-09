import time
import re


class BreadthFirst:

    WIDTH_OF_GRID = 15  # type: int
    HEIGHT_OF_GRID = 15  # type: int

    def __init__(self, master, grid):
        self.g = grid
        self.master = master

        self.starting_node = Node(0, 0)
        self.target_node = Node(0, 0)

        self.obstacle_nodes = []

        self.node_list = []

        for x in range(self.WIDTH_OF_GRID):
            for y in range(self.HEIGHT_OF_GRID):
                new_node = Node(x, y)
                self.node_list.append(new_node)

    def declare_starting_node(self, x, y):
        # from the x,y location, we can get the corresponding node in the list
        # given (x,y) = (0,5) we want the sixth element so index 5
        # given (x,y) = (1,5) we want the x * height + y ( i.e index 15 if height is 10)
        index = self.HEIGHT_OF_GRID * x + y
        # make the global variable start node point to the right index inside node list
        self.starting_node = self.node_list[index]
        self.modify_label("red", self.starting_node)

    def declare_target_node(self, x, y):
        # from the x,y location, we can get the corresponding node in the list
        # given (x,y) = (0,5) we want the sixth element so index 5
        # given (x,y) = (1,5) we want the x * height + y ( i.e index 15 if height is 10)
        index = self.HEIGHT_OF_GRID * x + y
        # make the global variable start node point to the right index inside node list
        self.target_node = self.node_list[index]
        self.modify_label("green", self.target_node)

    def build_tree_and_search(self):

        # list of nodes to visit in order of breadth
        # the open_nodes in a way represent the tree
        open_nodes = []

        # list of visited nodes
        closed_nodes = []

        # at the start the starting node is the root of the tree and is therefore the only element in open nodes
        open_nodes.append(self.starting_node)

        while True:

            # the current node is always the next node in the open nodes to implement a breadth first search
            current_node = open_nodes[0]

            if current_node is not self.starting_node:
                self.modify_label("blue", current_node)

            # now that we have a new current node, update the open nodes and closed node list
            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            # get all the neighbours of the current node, this will be the next breadth of the current node
            neighbours = self.get_neighbours(current_node)

            # check if the neighbours of the current node contain the target node
            # this condition is a success condition
            if self.target_node in neighbours:
                self.target_node.parent_node = current_node
                break

            # check if the neighbours are already in the tree somewhere
            # if so, do not add them again, remove them from the neighbours list
            for neighbour in neighbours:

                if neighbour not in open_nodes and neighbour not in closed_nodes \
                        and neighbour not in self.obstacle_nodes:

                    # mark the node as added to the tree
                    open_nodes.append(neighbour)

                    # set the parent node of the neighbour to be the current node
                    neighbour.parent_node = current_node

        # now that we have exited the while loop, we have set the parent node of the target node
        # this means that we can traverse the graph from the target to the starting node to draw the path

        print("found target")

    def draw_path(self):
        print("\n PATH FOUND: ")
        current_node = self.target_node
        while current_node.parent_node is not None:
            print("(x,y) : (%d, %d)" % (current_node.x_cord, current_node.y_cord))
            self.modify_label("green", current_node)
            current_node = current_node.parent_node
        print("(x,y) : (%d, %d)" % (current_node.x_cord, current_node.y_cord))

    def get_neighbours(self, node):
        # initialize the returned list of neighbours
        neighbours = []

        # get the index of the node in the node list
        index = node.x_cord * self.HEIGHT_OF_GRID + node.y_cord

        # get the max index

        # we now populate a list of at most 8 nodes from node list
        # we will name the 8 indices N, NE, W, SE, S, SW, W, NW
        #           NW  N  NE
        #             \ | /
        #        W  --  *  -- E
        #             / | \
        #           SW  S  SE

        N_index = index + 1
        NE_index = index + self.HEIGHT_OF_GRID + 1
        E_index = index + self.HEIGHT_OF_GRID
        SE_index = index + self.HEIGHT_OF_GRID - 1
        S_index = index - 1
        SW_index = index - self.HEIGHT_OF_GRID - 1
        W_index = index - self.HEIGHT_OF_GRID
        NW_index = index - self.HEIGHT_OF_GRID + 1

        valid_indices = [N_index, NE_index, E_index, SE_index, S_index, SW_index, W_index, NW_index]

        # if the node hugs the top border
        if node.y_cord == self.HEIGHT_OF_GRID - 1:
            print("in the top border")
            if NW_index in valid_indices:
                valid_indices.remove(NW_index)
            if N_index in valid_indices:
                valid_indices.remove(N_index)
            if NE_index in valid_indices:
                valid_indices.remove(NE_index)

        # if the node hugs the bottom border
        if node.y_cord == 0:
            print("in the bottom border")
            if SE_index in valid_indices:
                valid_indices.remove(SE_index)
            if S_index in valid_indices:
                valid_indices.remove(S_index)
            if SW_index in valid_indices:
                valid_indices.remove(SW_index)

        # if the node hugs the left border
        if node.x_cord == 0:
            print("in the left border")
            if SW_index in valid_indices:
                valid_indices.remove(SW_index)
            if W_index in valid_indices:
                valid_indices.remove(W_index)
            if NW_index in valid_indices:
                valid_indices.remove(NW_index)

        # if the node hugs the right border
        if node.x_cord == self.WIDTH_OF_GRID - 1:
            print("in the right border")
            if NE_index in valid_indices:
                valid_indices.remove(NE_index)
            if E_index in valid_indices:
                valid_indices.remove(E_index)
            if SE_index in valid_indices:
                valid_indices.remove(SE_index)

        # now we have all the valid indices and we can populate the neighbour list and return it
        for i in valid_indices:
            neighbours.append(self.node_list[i])

        return neighbours

    def modify_label(self, color, node):
        index = self.HEIGHT_OF_GRID * node.y_cord + node.x_cord
        print(index)
        label = self.g.labels[index]
        label.config(bg="%s" % color)
        self.master.update()
        time.sleep(0.02)


class Node:

    x_cord = 0
    y_cord = 0

    def __init__(self, x, y):
        # The parent node inside the tree
        self.parent_node = None
        self.x_cord = x
        self.y_cord = y


