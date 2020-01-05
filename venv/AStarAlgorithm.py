from Node import Node

WIDTH_OF_GRID = 10   # type: int
HEIGHT_OF_GRID = 10  # type: int

# constant list of nodes holding all the nodes on the grid
node_list = []

# initialize the starting node and the target node
# these variables will later point to a node inside the node list above
starting_node = Node(0,0)
target_node = Node(0,0)

# Create the list of nodes from the grid height and width
# The list will contains the nodes in order of columns starting from
# the left-most column and going up the column in y values
for x in range(WIDTH_OF_GRID):
    for y in range(HEIGHT_OF_GRID):
        new_node = Node(x, y)
        node_list.append(new_node)


def declare_starting_node(x,y):
    # from the x,y location, we can get the corresponding node in the list
    # given (x,y) = (0,5) we want the sixth element so index 5
    # given (x,y) = (1,5) we want the x * height + y ( i.e index 15 if height is 10)
    index = HEIGHT_OF_GRID * x + y
    # make the global variable start node point to the right index inside node list
    global starting_node
    starting_node = node_list[index]


def declare_target_node(x,y):
    # from the x,y location, we can get the corresponding node in the list
    # given (x,y) = (0,5) we want the sixth element so index 5
    # given (x,y) = (1,5) we want the x * height + y ( i.e index 15 if height is 10)
    index = HEIGHT_OF_GRID * x + y
    # make the global variable start node point to the right index inside node list
    global target_node
    target_node = node_list[index]


"""This method return at most 8 nodes, 5 nodes if it hugs a border and at least 3 nodes if it is a corner"""


def get_neighbours(node):
    # initialize the returned list of neighbours
    neighbours = []

    # get the index of the node in the node list
    index = node.x_cord * HEIGHT_OF_GRID + node.y_cord

    # get the max index

    # we now populate a list of at most 8 nodes from node list
    # we will name the 8 indices N, NE, W, SE, S, SW, W, NW
    #           NW  N  NE
    #             \ | /
    #        W  --  *  -- E
    #             / | \
    #           SW  S  SE

    N_index = index + 1
    NE_index = index + HEIGHT_OF_GRID + 1
    E_index = index + HEIGHT_OF_GRID
    SE_index = index + HEIGHT_OF_GRID - 1
    S_index = index - 1
    SW_index = index - HEIGHT_OF_GRID - 1
    W_index = index - HEIGHT_OF_GRID
    NW_index = index - HEIGHT_OF_GRID + 1

    valid_indices = [N_index, NE_index, E_index, SE_index, S_index, SW_index, W_index, NW_index]

    # if the node hugs the top border
    if node.y_cord == HEIGHT_OF_GRID - 1:
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
    if node.x_cord == HEIGHT_OF_GRID - 1:
        print("in the right border")
        if NE_index in valid_indices:
            valid_indices.remove(NE_index)
        if E_index in valid_indices:
            valid_indices.remove(E_index)
        if SE_index in valid_indices:
            valid_indices.remove(SE_index)

    # now we have all the valid indices and we can populate the neighbour list and return it
    for i in valid_indices:
        neighbours.append(node_list[i])

    return neighbours


declare_starting_node(0, 0)
declare_target_node(HEIGHT_OF_GRID - 3, HEIGHT_OF_GRID - 1)
starting_node.compute_g_h_f(None, target_node)
target_node.compute_g_h_f(None, target_node)


def a_star_algorithm():
    # list of nodes to be visited
    open_nodes = []

    # list of nodes already visited
    closed_nodes = []

    open_nodes.append(starting_node)

    # outer loop that runs until we get to the target
    while True:
        print("Open nodes:")
        for open in open_nodes:
            print("(x,y) : (%d, %d)  f cost = %d" % (open.x_cord, open.y_cord, open.f_value))
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

        # exit the while loop and the algorithm when we are at the target node
        if current_node == target_node:
            return

        # get all the neighbours as a list of neighbours
        current_neighbours = get_neighbours(current_node)
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
                neighbour.parent_node = current_node
                neighbour.compute_g_h_f(current_node, target_node)
                open_nodes.append(neighbour)
            # if we had already discovered this node, check if the path from the current node as
            # parent node to the neighbour yields a lesser f value. If som change it.
            else:
                temp_node = Node(neighbour.x_cord, neighbour.y_cord)
                temp_node.parent_node = current_node
                temp_node.compute_g_h_f(current_node, target_node)
                # if the temporary f value is less, swap the parent node of the neighbour to the current node
                if temp_node.f_value < neighbour.f_value:
                    neighbour.parent_node = current_node

    # end of a star algorithm
    return


def draw_path():
    print("\n PATH FOUND: ")
    current_node = target_node
    while current_node.parent_node is not None:
        print("(x,y) : (%d, %d)" % (current_node.x_cord, current_node.y_cord))
        current_node = current_node.parent_node
    print("(x,y) : (%d, %d)" % (current_node.x_cord, current_node.y_cord))


a_star_algorithm()
draw_path()






