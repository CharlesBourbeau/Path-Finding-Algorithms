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


