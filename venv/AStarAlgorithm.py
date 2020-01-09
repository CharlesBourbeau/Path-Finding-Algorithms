import time
import re


class AStarAlgorithm:

    WIDTH_OF_GRID = 15  # type: int
    HEIGHT_OF_GRID = 15  # type: int

    def __init__(self, master, grid):
        self.g = grid
        self.master = master
        # constant list of nodes holding all the nodes on the grid
        self.node_list = []

        # initialize the starting node and the target node
        # these variables will later point to a node inside the node list above
        self.starting_node = Node(0, 0)
        self.target_node = Node(0, 0)
        self.obstacle_nodes = []

        # Create the list of nodes from the grid height and width
        # The list will contains the nodes in order of columns starting from
        # the left-most column and going up the column in y values
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

    """This method return at most 8 nodes, 5 nodes if it hugs a border and at least 3 nodes if it is a corner"""

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

    def a_star_algorithm(self):
        # list of nodes to be visited
        open_nodes = []

        # list of nodes already visited
        closed_nodes = []

        open_nodes.append(self.starting_node)

        # outer loop that runs until we get to the target
        while True:
            print("Open nodes:")
            for open_node in open_nodes:
                print("(x,y) : (%d, %d)  f cost = %d" % (open_node.x_cord, open_node.y_cord, open_node.f_value))
            print("\n\n")

            # current node becomes the current node with the lowest f value
            # assume that the first element of open nodes has the lowest and then compare
            current_node = open_nodes[0]
            for node in open_nodes:
                if node.f_value < current_node.f_value:
                    current_node = node

            print("Current node: ")
            print("(x,y) : (%d, %d)\n" % (current_node.x_cord, current_node.y_cord))
            # now we have a new current node which we visit, hence we remove it from open to closed nodes
            open_nodes.remove(current_node)
            closed_nodes.append(current_node)
            if current_node is not self.starting_node:
                self.modify_label("blue", current_node)

            # exit the while loop and the algorithm when we are at the target node
            if current_node == self.target_node:
                return

            # get all the neighbours as a list of neighbours
            current_neighbours = self.get_neighbours(current_node)
            print("Neigbours: ")
            for neighbour in current_neighbours:
                print("(x,y) : (%d, %d)" % (neighbour.x_cord, neighbour.y_cord))
            print("\n\n")

            for neighbour in current_neighbours:
                # if the node has already been visited, skip it
                if neighbour in closed_nodes:
                    continue

                # if we are first discovering this node, set the parent and compute the f cost
                if neighbour not in open_nodes:
                    # if the node is an obstacle, we should not visit it since it is unreachable
                    if neighbour in self.obstacle_nodes:
                        continue
                    neighbour.parent_node = current_node
                    neighbour.compute_g_h_f(current_node, self.target_node)
                    open_nodes.append(neighbour)
                    if neighbour is not self.target_node:
                        self.modify_label("light blue", neighbour)
                # if we had already discovered this node, check if the path from the current node as
                # parent node to the neighbour yields a lesser f value. If so change it.
                else:
                    temp_node = Node(neighbour.x_cord, neighbour.y_cord)
                    temp_node.parent_node = current_node
                    temp_node.compute_g_h_f(current_node, self.target_node)
                    # if the temporary f value is less, swap the parent node of the neighbour to the current node
                    if temp_node.f_value < neighbour.f_value:
                        # set the new parent node of the neighbour
                        neighbour.parent_node = current_node
                        # recalculate its updated f value with the new parent
                        neighbour.compute_g_h_f(current_node, self.target_node)

        # end of a star algorithm
        return

    def draw_path(self):
        print("\n PATH FOUND: ")
        current_node = self.target_node
        while current_node.parent_node is not None:
            print("(x,y) : (%d, %d)" % (current_node.x_cord, current_node.y_cord))
            self.modify_label("green", current_node)
            current_node = current_node.parent_node
        print("(x,y) : (%d, %d)" % (current_node.x_cord, current_node.y_cord))

    def modify_label(self, color, node):
        index = self.HEIGHT_OF_GRID * node.y_cord + node.x_cord
        print(index)
        label = self.g.labels[index]
        label.config(bg="%s" % color)
        label.config(text="%d" % node.f_value)
        self.master.update()
        time.sleep(0.02)


class Node:
    # initialize the h and g value needed to compute the f value
    h_value = 0
    g_value = 0

    f_value = 0

    # initialize the parent node used to compute the g_value and reconstruct the path
    parent_node = None

    # initialize the coordinate values
    # these value will be adjusted once a node is added to the grid
    x_cord = 0
    y_cord = 0

    # Constructor
    def __init__(self, a_x_cord, a_y_cord):
        self.x_cord = a_x_cord
        self.y_cord = a_y_cord

    # Reset a node
    def reset_node(self):
        self.f_value = 0
        self.g_value = 0
        self.h_value = 0
        self.parent_node = None

    """For both the computation of the h value and the g vale we will use the 
    such a strategy that we evaluate the proportional weight of a diagonal mode over
    a lateral move to be sqrt(2)/1, or for approximation 14/10 Meaning the 4 lateral 
    moves have a weight proportional to 10 and the diagonal moves a weight proportional to 14
    So the strategy is to first compute the minimum out of the y difference and the x difference,
    move diagonally by the minimum and then move lateraly for the remaining x or y cord"""

    def compute_h_value(self, target_node):
        # we first determine if we should reduce the y difference or the x difference
        x_difference = abs(self.x_cord - target_node.x_cord)
        y_difference = abs(self.y_cord - target_node.y_cord)
        if x_difference < y_difference:
            # we want to decrease x diagonally and then y laterally
            self.h_value = x_difference * 14
            # we now need to consider that the y difference has decreased
            # by exactly the x difference since we moved diagonally
            y_difference -= x_difference
            self.h_value += y_difference * 10

        else:  # y_difference <= x_difference:
            # we want to decrease y diagonally and then x laterally
            self.h_value = y_difference * 14
            # we now need to consider that the x difference has decreased
            # by exactly the y difference since we moved diagonally
            x_difference -= y_difference
            self.h_value += x_difference * 10

    def compute_g_value(self, parent_node):
        # if the parent node is node, it if the start node and the g value is 0
        if parent_node is None:
            self.g_value = 0
            return

        # we first determine if we should reduce the y difference or the x difference
        x_difference = abs(self.x_cord - parent_node.x_cord)
        y_difference = abs(self.y_cord - parent_node.y_cord)
        if x_difference < y_difference:
            # we want to decrease x diagonally and then y laterally
            self.g_value = x_difference * 14
            # we now need to consider that the y difference has decreased
            # by exactly the x difference since we moved diagonally
            y_difference -= x_difference
            self.g_value += y_difference * 10

        else:  # y_difference <= x_difference
            # we want to decrease y diagonally and then x laterally
            self.g_value = y_difference * 14
            # we now need to consider that the x difference has decreased
            # by exactly the y difference since we moved diagonally
            x_difference -= y_difference
            self.g_value += x_difference * 10

        # now we add the parent g value to this value to update the path
        if parent_node is not None:
            self.g_value += parent_node.g_value

    def compute_g_h_f(self, parent_node, target_node):
        self.compute_g_value(parent_node)
        self.compute_h_value(target_node)
        self.f_value = self.g_value + self.h_value